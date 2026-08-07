# Performance Report

## Measured Results

- Application startup and shutdown:
  - exit code: `0`
  - elapsed time: `0.004839s`
  - max resident memory: `16512 KB`
- End-to-end engineering workflow benchmark:
  - elapsed time: `0.02496s`
  - traced current memory: `113598 bytes`
  - traced peak memory: `122803 bytes`
  - renderables produced: `2`
  - engineering calculation result: `20.0 MPa`
  - simulation status: `completed`
- Release-candidate suite runtime:
  - `4 passed in 0.33s`
- Full regression runtime:
  - `113 passed in 1.10s`

## Interpretation

- Startup overhead is minimal for the current headless runtime.
- The integrated workflow completes well under one second and shows no abnormal memory growth.
- Simulation orchestration, AI review, rendering, persistence, and engineering reporting all complete within the benchmarked RC1 workflow.

## Conclusion

RC1 satisfies practical performance and memory expectations for the deterministic headless scope implemented in this repository.
