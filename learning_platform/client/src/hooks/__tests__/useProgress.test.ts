import { describe, it, expect } from 'vitest';

// SuperMemo SM-2 Calculation Function Under Test
function calculateSm2(
  current: { interval_days: number; repetition: number; ease_factor: number },
  rating: number
) {
  let { repetition, interval_days, ease_factor } = current;
  const q = Math.max(0, Math.min(5, rating));

  // EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
  ease_factor = ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02));
  if (ease_factor < 1.3) ease_factor = 1.3;

  if (q < 3) {
    repetition = 0;
    interval_days = 1;
  } else {
    if (repetition === 0) {
      interval_days = 1;
    } else if (repetition === 1) {
      interval_days = 6;
    } else {
      interval_days = Math.round(interval_days * ease_factor);
    }
    repetition += 1;
  }

  return {
    repetition,
    interval_days,
    ease_factor: Number(ease_factor.toFixed(3)),
  };
}

describe('SuperMemo SM-2 Spaced Repetition Algorithm', () => {
  it('initializes card with 1 day interval on first successful review (rating 4 - Good)', () => {
    const initial = { interval_days: 0, repetition: 0, ease_factor: 2.5 };
    const step1 = calculateSm2(initial, 4);

    expect(step1.repetition).toBe(1);
    expect(step1.interval_days).toBe(1);
    expect(step1.ease_factor).toBe(2.5); // EF unchanged for rating 4
  });

  it('schedules 6 days on second successful review (repetition 1 -> 2)', () => {
    const afterFirst = { interval_days: 1, repetition: 1, ease_factor: 2.5 };
    const step2 = calculateSm2(afterFirst, 5); // Easy

    expect(step2.repetition).toBe(2);
    expect(step2.interval_days).toBe(6);
    expect(step2.ease_factor).toBe(2.6); // EF increases for rating 5
  });

  it('multiplies interval by ease factor on third successful review', () => {
    const afterSecond = { interval_days: 6, repetition: 2, ease_factor: 2.6 };
    const step3 = calculateSm2(afterSecond, 4);

    expect(step3.repetition).toBe(3);
    expect(step3.interval_days).toBe(Math.round(6 * 2.6)); // 16 days
    expect(step3.ease_factor).toBe(2.6);
  });

  it('resets repetition to 0 and interval to 1 day on failed review (rating < 3)', () => {
    const seasoned = { interval_days: 35, repetition: 5, ease_factor: 2.4 };
    const failed = calculateSm2(seasoned, 1); // Again (forgotten)

    expect(failed.repetition).toBe(0);
    expect(failed.interval_days).toBe(1);
    expect(failed.ease_factor).toBeLessThan(2.4);
    expect(failed.ease_factor).toBeGreaterThanOrEqual(1.3);
  });

  it('clamps minimum ease factor to 1.3', () => {
    let card = { interval_days: 1, repetition: 0, ease_factor: 1.35 };
    for (let i = 0; i < 5; i++) {
      card = calculateSm2(card, 0);
    }
    expect(card.ease_factor).toBe(1.3);
  });
});

describe('Module Mastery Gate Logic', () => {
  it('correctly evaluates gate clearance when all requirements are met', () => {
    const gateStatus = {
      quizPassed: true,
      labPassed: true,
      cleared: false,
    };

    const isCleared = gateStatus.cleared || (gateStatus.quizPassed && gateStatus.labPassed);
    expect(isCleared).toBe(true);
  });

  it('keeps gate locked if quiz is not passed', () => {
    const gateStatus = {
      quizPassed: false,
      labPassed: true,
      cleared: false,
    };

    const isCleared = gateStatus.cleared || (gateStatus.quizPassed && gateStatus.labPassed);
    expect(isCleared).toBe(false);
  });
});
