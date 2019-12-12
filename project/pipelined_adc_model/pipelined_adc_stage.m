% pipelined ADC model

% MATLAB Coder directive
%#codegen

classdef pipelined_adc_stage < matlab.System

    % Public, tunable properties
    properties (Nontunable)
      comp_offsets = zeros(6, 1);
      sigma_noise = 0;
      delta_G = 0;
    end

    properties(DiscreteState)
      x;
      q;
    end

    % Pre-computed constants
    properties(Access = private)
      thresholds
      levels
    end

  methods
    function obj = pipelined_adc_stage(varargin)
      setProperties(obj,nargin,varargin{:});
    end
  end

  methods(Access = protected)

    % - getNumInputsImpl: number of inputs passed to step and setup methods -
    function numIn = getNumInputsImpl(~)
      numIn = 1;
    end

    % - getNumOutputsImpl: number of outputs returned by step method -
    function numOut = getNumOutputsImpl(~)
      numOut = 2;
    end

    % - validatePropertiesImpl: validate property values -
    function validatePropertiesImpl(obj)
      assert(isnumeric(obj.comp_offsets) && isreal(obj.comp_offsets) ...
             && isrow(obj.comp_offsets) && numel(obj.comp_offsets) == 6);
      assert(isnumeric(obj.sigma_noise) && isscalar(obj.sigma_noise) ...
             && isreal(obj.sigma_noise) && obj.sigma_noise >= 0.0);
    end

    % - validateInputsImpl: validate inputs to step method -
    function validateInputsImpl(~, u)
      assert(isnumeric(u) && isreal(u) && isscalar(u), ...
             'Input "u" must be a scalar number.');
    end

    % - setupImpl: initialize system object -
    function setupImpl(obj)
      % Perform one-time calculations, such as computing constants

      % sub-ADC thresholds
      th = (0:5)/4.0 - 0.625 + obj.comp_offsets;
      % sub-DAC levels
      lv = (0:6)/4.0 - 0.75;

      assert(isnumeric(th) && isreal(th) && isrow(th));
      assert(isnumeric(lv) && isreal(lv) && isrow(lv));
      assert(numel(th) + 1 == numel(lv));
      obj.thresholds = th;
      obj.levels = lv;
    end

    % - resetImpl: reset system object states -
    function resetImpl(obj)
      % Initialize / reset discrete-state properties
      obj.x = 0;
      obj.q = 0;
    end

    % - stepImp: system output and state update equations -
    function [y, q] = stepImpl(obj, u)
      % Implement algorithm.
      % Calculate y as a function of input u and discrete states.

      % outputs are one step delayed w.r.t. inputs
      y = obj.x;
      q = obj.q;

      % calculate next outputs
      obj.q = sub_adc_impl(obj, u);
      obj.x = mdac_impl(obj, u, obj.q);
    end

    function q = sub_adc_impl(obj, u)
      % sub-ADC
      q = sum(u >= obj.thresholds);
    end

    function y = mdac_impl(obj, u, q)
      u = max(min(u, +1), -1);

      % MDAC gain stage with output saturation
      y = 4.0 * (1 + obj.delta_G) * (u - obj.levels(q + 1));
      y = y + obj.sigma_noise * randn();
      y = max(min(y, +1), -1);
    end

  end

end
