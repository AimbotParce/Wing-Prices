import numpy as np
import pandas as pd

wings = pd.read_excel("Wings.xlsx", sheet_name="Wings")

MAX = 500
MIN = wings[wings["Chicken Wing Count (w)"] <= MAX].iloc[0]["Chicken Wing Count (w)"]

for i in range(MIN, MAX):
    lower = wings[wings["Chicken Wing Count (w)"] <= i]
    counts = lower["Chicken Wing Count (w)"].values
    prices = lower["Price ($)"].values
    # We want all values of x, y, z, ... such that c1*x + c2*y + c3*z + ... = i and x, y, z, ... are positive integers
    # Easy way: Meshgrid and brute force, but this grows extremely quickly

    # Hard way: Compute the base for the hyperplane, and then find all the solutions. counts forms a normal vector
    # to the hyperplane. We also know that for i > 4, at least one solution exists.
    # We must find an integer basis for the hyperplane, which will ensure that all solutions are integers.
    # There's two problems I see we need to solve: Finding an integer basis, and finding the first integer solution.
    # The second can be done with a simple algorithm, subtracting the biggest possible value each time until we get to zero.

    def findSolution(current: int, subtractions: list[int] = []) -> list[int]:
        """
        Depth-first search to find the first integer solution to the hyperplane.

        We can't use this algotihm to find all solutions, because it will explore many paths that are not solutions.
        After i=40 or so, it becomes too slow to be useful.
        """
        if current == 0:
            # Convert the subtractions to a vector which says how many of each wing we need
            vector = np.zeros_like(counts, dtype=int)
            for subtraction in subtractions:
                vector[np.where(counts == subtraction)[0][0]] += 1
            return vector
        # We want to start with the biggest value, as it is the most likely to already be a solution
        for i in reversed(range(len(counts))):
            if current - counts[i] >= 0:
                sol = findSolution(current - counts[i], subtractions + [counts[i]])
                if sol is not None:
                    return sol
        return None

    def string(solution: list[int]) -> str:
        """
        Convert a solution to a string.
        """
        return " + ".join([f"{solution[i]}x{counts[i]} Pack" for i in range(len(counts)) if solution[i] != 0])

    particular_solution = findSolution(i)
    if particular_solution is None:
        print(f"{i}) No solution")
        continue
    elif len(counts) == 1:  # There won't be any other solutions
        print(f"{i}) Best: {string(particular_solution)}")
        continue
    print(f"{i} = {string(particular_solution)}")

    # Let's now try to find the basis for the hyperplane. Let's start with a single vector from the basis:
    # Given that the normal vector (counts) is already integer, we can find a perpendicular vector by swapping the
    # x and y coordinates and negating one of them, as well as setting the other to zero.
    # basis1 = np.zeros_like(counts, dtype=int)
    # basis1[0] = counts[1]
    # basis1[1] = -counts[0]
    # # Ensure that they are perpendicular
    # assert np.dot(counts, basis1) == 0

    # Let's not forget that we do have another basis for this space, the euclidean basis, which, given that the normal
    # vector is an integer vector with no zeros, we know that it is not colinear with any euclidean basis vector.
    # This means that we can implement an alternative Gram-Schmidt algorithm to find more basis vectors.
    #
    # The Gram-Schmidt algorithm is as follows:
    # *) Have a list of linearly independent vectors (the euclidean in our case), and a subset of vectors that form
    #    an orthogonal basis for a subspace (in our case, the normal vector and one perpendicular vector that we already
    #    found, even though we don't need it).
    # *) Repeat the following for each vector in the list of linearly independent vectors (the euclidean in our case):
    # 1) For each vector in the orthogonal basis, find the projection of the current vector onto it.
    # 2) Subtract the projection from the current vector.
    # 3) Add the resulting vector to the orthogonal basis.
    # The formula should look something like this:
    # vec{e} = vec{e} - (vec{e} . vec{v}) * vec{v} / (vec{v} . vec{v}) # . is dot product and * is scalar multiplication
    #
    # This is easy to see in the following example:
    # Let the linearly independent vectors be [1, 0, 0], [0, 1, 0], [0, 0, 1], and the orthogonal basis be [1, 1, 1].
    # We want to complete the orthogonal basis to the euclidean basis.
    # *) We start with e = [1, 0, 0].
    # 1) [1, 0, 0] - ([1, 0, 0].[1, 1, 1]) * [1, 1, 1] / ([1, 1, 1].[1, 1, 1]) = [1, 0, 0] - 1 * [1, 1, 1] / 3 = [2/3, -1/3, -1/3]
    # *) Then, we update the new orthogonal basis to be [1, 1, 1], [2/3, -1/3, -1/3].
    # *) We then repeat the process for e = [0, 1, 0], having in mind that this must be repeated for the two vectors in the orthogonal basis.
    # 1) [0, 1, 0] - ([0, 1, 0].[1, 1, 1]) * [1, 1, 1] / ([1, 1, 1].[1, 1, 1]) = [0, 1, 0] - 1 * [1, 1, 1] / 3 = [-1/3, 2/3, -1/3]
    # 2) [-1/3, 2/3, -1/3] - ([-1/3, 2/3, -1/3].[2/3, -1/3, -1/3]) * [2/3, -1/3, -1/3] / ([2/3, -1/3, -1/3].[2/3, -1/3, -1/3]) =
    #    = [-1/3, 2/3, -1/3] - (-2/9 - 2/9 + 1/9) * [2/3, -1/3, -1/3] / (4/9 + 1/9 + 1/9) = [-1/3, 2/3, -1/3] - (-1/3) * [2/3, -1/3, -1/3] / (2/3) =
    #    = [-1/3, 2/3, -1/3] + (1/2) * [2/3, -1/3, -1/3] = [0, 1/2, -1/2]
    # *) Then, we update the new orthogonal basis to be [1, 1, 1], [2/3, -1/3, -1/3], [0, 1/2, -1/2].
    # Finally, given that we have 3 linearly independent vectors, we know that we have found an orthogonal basis for the whole space.
    # To check, one can perform the dot product between each vector and the other, and see that they are all zero.
    # [1, 1, 1].[2/3, -1/3, -1/3] = 2/3 - 1/3 - 1/3 = 0
    # [1, 1, 1].[0, 1/2, -1/2] = 0 + 1/2 - 1/2 = 0
    # [2/3, -1/3, -1/3].[0, 1/2, -1/2] = 0 - 1/6 + 1/6 = 0
    #
    # But here's the first problem: We are working with integers, and we want to find integer basis vectors. These vectors have
    # rational coordinates. My solution is simply to multiply the entire formula by the squared norm of the vector already
    # in the orthogonal basis, which will ensure that the coordinates are integers (given that components of the vector are, and
    # no square roots are involved).
    # The formula then becomes (to simplify, lets call (vec{v} . vec{v}) = ||v||^2 and vec{e} = e)
    # [ e = e - (e . v) * v / ||v||^2 ] * ||v||^2 -> e ||v||^2 = e * ||v||^2 - (e . v) * v
    # And the left side is a vector with no ovelap with any vector in the orthogonal basis, so we can call it e' and move on.
    # This is because e was, so k*e is.
    # e' = e * ||v||^2 - (e . v) * v
    #
    # On top of this, Gram-Schmidt also normalizes the vectors, which we don't want to do, as we want to keep the integer coordinates.
    # One thing we can try to do is to find the gcd of the coordinates of the vector, and divide them by it. This will ensure that
    # the coordinates are as small as possible, and will also ensure that the coordinates are integers.

    # Let's implement this. Start with the function that will reduce the coordinates of a vector to their gcd.
    def reduce(vec: np.ndarray) -> np.ndarray:
        gcd = np.gcd.reduce(vec)  # Wow, thanks copilot, I didn't know this existed xd
        return vec // gcd

    basis = [reduce(counts)]
    for j in range(len(counts)):
        e = np.zeros_like(counts, dtype=object)
        e[j] = 1  # The euclidean basis
        for v in basis:
            # Compute all of this first, as these will raise a warning if there's overflow
            vv = np.dot(v, v)
            ev = np.dot(e, v)
            vmax = ev * v.max()
            emax = e.max() * vv
            maxmax = emax + vmax

            e = e * vv - ev * v
        if np.dot(e, e) == 0:
            continue  # This means that the vector is linearly dependent of the orthogonal basis
        basis.append(reduce(e))
    assert len(basis) == len(counts)  # We have found a basis for the whole space

    # Now we have a basis for the hyperplane, the first vector of which is the normal vector. We must now explore
    # the hyperplane to find all integer solutions. All of this was only to reduce the dimensionality of the
    # problem by 1. I am sad :(
    # We still have some conditions to satisfy:
    # 1) All coordinates of the solutions must be positive (we can't have negative chicken wings)

    # We can assert that this method worked by creating an array of random coefficients for the vectors in the basis,
    # and multiplying them by the basis. This should give us a random vector in the subspace of the hyperplane.
    # Adding this vector to the particular solution, we should get a random solution to the hyperplane.
    # And this solution should satisfy the hyperplane equation, meaning that its dot product with the normal vector
    # should give us exactly i, the number of chicken wings we want.
    randomCoefficients = np.random.randint(0, 100, size=len(counts) - 1)
    # Find a solution with:
    sol = particular_solution + np.dot(randomCoefficients, basis[1:])
    count = np.dot(sol, counts)
    assert count == i, f"Count is {count} and should be {i}"
