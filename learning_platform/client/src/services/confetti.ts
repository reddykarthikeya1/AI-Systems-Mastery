import confetti from 'canvas-confetti';

/**
 * Fires celebratory confetti particle bursts for learner achievements.
 */
export function fireConfettiBurst(intensity: 'small' | 'medium' | 'grand' = 'medium') {
  try {
    if (typeof window === 'undefined') return;

    if (intensity === 'small') {
      confetti({
        particleCount: 40,
        spread: 50,
        origin: { y: 0.75 },
        colors: ['#10B981', '#3B82F6', '#6366F1', '#F59E0B'],
      });
    } else if (intensity === 'medium') {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.65 },
        colors: ['#10B981', '#06B6D4', '#8B5CF6', '#EC4899', '#F59E0B'],
      });
    } else {
      // Grand celebration (for course or module completion)
      const count = 200;
      const defaults = {
        origin: { y: 0.6 },
        colors: ['#10B981', '#3B82F6', '#8B5CF6', '#F59E0B', '#EF4444'],
      };

      const fire = (particleRatio: number, opts: confetti.Options) => {
        confetti({
          ...defaults,
          ...opts,
          particleCount: Math.floor(count * particleRatio),
        });
      };

      fire(0.25, { spread: 26, startVelocity: 55 });
      fire(0.2, { spread: 60 });
      fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
      fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
      fire(0.1, { spread: 120, startVelocity: 45 });
    }
  } catch (err) {
    console.debug('Confetti execution skipped:', err);
  }
}
