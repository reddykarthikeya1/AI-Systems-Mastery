# Debug Lab 09 - Symptoms

> A numerical differentiator and gradient-descent optimiser. Both produce answers for every input they are given.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_numerical_calculus.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - Smaller steps give better answers, as expected

```
    h=1e-02    forward err=6.010e-02   central err=1.000e-04
    h=1e-04    forward err=6.000e-04   central err=1.001e-08
    h=1e-06    forward err=6.002e-06   central err=7.892e-10
```

Both estimates improve as h shrinks, and the central difference is far more accurate at the same h. That is the textbook result: the forward difference has error proportional to h, the central difference to h squared.

**Ask yourself:** if smaller h is better, what is the best h?

---

## Section 2 - Past a point, smaller steps make it worse - then useless

```
    h=1e-10    estimate=12.000000992884        err=9.929e-07
    h=1e-13    estimate=11.990408665952        err=9.591e-03
    h=1e-15    estimate=11.990408665952        err=9.591e-03
    h=1e-17    estimate=0.000000000000         err=1.200e+01
```

The error falls, bottoms out, and then climbs. At the smallest step the estimate is not merely inaccurate; it has lost almost all its significant digits.

**Ask yourself:** `f(x+h)` and `f(x-h)` are nearly equal numbers. What happens to the relative error when you subtract two nearly equal floats, and then divide by something tiny?

---

## Section 3 - Gradient descent reports success while diverging

```
    lr=0.1   final x=1.532496e-06             |x| shrank: True
    lr=0.9   final x=1.532496e-06             |x| shrank: True
    lr=1.01  final x=3.281031e+00             |x| shrank: False
```

Read the last row. With a learning rate of 1.01 the final value is enormous - the optimiser has run away from the minimum - and yet no warning is produced and the function returns normally.

**Ask yourself:** for f(x) = x^2 the update is x <- x(1 - 2*lr). For which learning rates does that shrink x, and what happens at exactly the boundary?

---
