function h = run_pipelined_adc

  fs = 1;                               % sampling frequency
  T = 1/fs;                             % sampling period

  N = 2^14;                             % number of samples
  cycles = round(0.45*N);               % number of cycles
  fx = cycles * fs/N;

  % construct waveforms
  f = (0:N/2)*fs;
  Nstab = N/2^8;
  t = 0:T:(N+Nstab-1)*T;
  A = 0.5;
  x = A * sin(2*pi * fx*t);

  % simulate system
  simOut = sim( ...
      'pipelined_adc', ...
      'StopTime', sprintf('%g', max(t)), ...
      'Solver', 'FixedStepDiscrete', ...
      'LoadExternalInput', 'on', ...
      'ExternalInput', '[t'', x'']', ...
      'SaveTime', 'on', ...
      'SaveOutput', 'on', ...
      'SaveFormat', 'Array', ...
      'LimitDataPoints', 'off', ...
      'SrcWorkspace', 'current');
  tout = simOut.get('tout');
  yout = simOut.get('yout');
  y = squeeze(yout);
  y = y(1+Nstab:end);
  y = y/pow2(ceil(log2(max(abs(y)))));

  % calculate spectrum
  s = fft(y);                           % spectrum
  s(end/2+2:end, :) = [];               % frequencies 0 to fs/2
  s = s .* conj(s);                     % power
  s(1) = 0.5*s(1);                      % dc fix
  s(end) = 0.5*s(end);
  s = s/N/N;

  % plot spectrum
  h  = [figure];
  plot(f, 10*log10(eps+s));

  P_S = s(cycles+1);
  P_N = sum([s(2:cycles); s(cycles+2:end)]);
  SNDR = 10*log10(P_S/P_N)
  SFDR = 10*log10(P_S / max([s(2:cycles); s(cycles+2:end)]))

end
