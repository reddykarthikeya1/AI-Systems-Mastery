# 🐣 Interactive Foundations Playground: Linear Algebra in Models (PCA & OLS)

> *"Two formulas power 80% of classical machine learning: Principal Component Analysis (eigenvectors of covariance) and Ordinary Least Squares ($(X^T X)^{-1} X^T y$)."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. PCA: The Perfect Camera Angle

Imagine a flock of birds flying in 3D space:
- If you take a photo from below, the flock might look like a tight blob.
- If you walk around and photograph from the side, you capture the **full wingspan and spread**.
- **Principal Component Analysis (PCA)** automatically finds that exact best camera angle!
  1. Center the data so the center of mass is at the origin $(0, 0)$.
  2. Compute the **Covariance Matrix** to see which directions vary together.
  3. Find the **Eigenvectors** of the covariance matrix. The eigenvector with the largest eigenvalue is your primary camera angle (**PC1**)!

---

## 2. Ordinary Least Squares (OLS): Dropping the Plumb Line

Suppose you want to predict house price $y$ from square footage and bedrooms: $X w \approx y$.
- Since real-world data has noise, no weight vector $w$ can make $X w$ equal $y$ exactly.
- The space of all possible predictions $X w$ is a flat floor called the **Column Space** $C(X)$.
- The vector $y$ floats in the air above the floor.
- To make the error $e = y - X w$ as tiny as possible, we drop a **perpendicular plumb line** onto the floor.
- When the error is perpendicular to every column:
$$X^T (y - X w) = 0 \implies X^T X w = X^T y \implies w = (X^T X)^{-1} X^T y$$
This is the legendary **Normal Equation**!

---

## 3. Ridge Regression: The Invertibility Safety Net

What happens if two features are identical (e.g., house size in sq ft and sq meters)?
- The matrix $X^T X$ is singular and **cannot be inverted**!
- **Ridge Regression** adds a tiny diagonal ridge $\lambda I$:
$$w_{ridge} = (X^T X + \lambda I)^{-1} X^T y$$
- Since $X^T X$ is positive semi-definite and $\lambda I$ is strictly positive definite, $(X^T X + \lambda I)$ is **always guaranteed invertible**.
