function h = run_pipelined_adc_stage

% RUN_PIPELINED_ADC_STAGE  Run a single stage and create residue plot.

  h = [];

  simOut = sim('pipelined_adc_stage_test');
  val = simOut.results.signals.values;

  h = [h, figure];
  plot(val(:, 1), val(:, 2));
  axis([-1, +1, -1, +1]);
  xlabel('Input');
  ylabel('Output');

end
