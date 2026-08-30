## What

<!-- One-sentence description of the change -->

## Why

<!-- Which user need (job) does this address? -->

## .jtbd/ evidence

<!-- Which interview data or patterns informed this change? Reference specific .jtbd/ files if applicable. If this is infrastructure/meta work, say "N/A — repo infrastructure." -->

## Test plan

- [ ] Tested with example transcript (`examples/sample-transcript.txt`)
- [ ] Tested with a real interview transcript
- [ ] `python3 scripts/validate.py` passes — it validates every `.yml` in the repo,
      including ones you generated but have not staged yet. See TESTING.md.
- [ ] `python3 scripts/validate.py --self-test` passes, if you changed the validator
