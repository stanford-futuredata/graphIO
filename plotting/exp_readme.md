# Setup for all parts of the solver
First create a virtual environment:

    python3 -m virtualenv venv
    source venv/bin/activate

Next install the python requirements

    pip3 install -r requirements.txt

## For the ILP solver and lower bound:

### Install Gurobi
We need to set up gurobi. You need to have gurobi installed such that gurobipy can be successfully imported. Gurobi distributes free academic licenses. Gurobi typically comes with OSX installations. Install the most recent version of the Gurobi solver from [here](http://www.gurobi.com/downloads/gurobi-optimizer).

For a linux machine you can do:

    wget https://packages.gurobi.com/8.1/gurobi8.1.1_linux64.tar.gz
    tar -xvf gurobi8.1.1_linux64.tar.gz

Then add the following environment variables to your startup file:

    export GUROBI_HOME="<your path here>/gurobi811/linux64"
    export PATH="${PATH}:${GUROBI_HOME}/bin"
    export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"

Then install your license via:

    grbgetkey <your license here>

You may then need to add this line to your start file: 

    export GRB_LICENSE_FILE="<your license path here>"

Finally from the linux64 directory run:

    python3 setup.py install

### Install Metis
You also need the graph partitioning software Metis installed [see here](http://glaros.dtc.umn.edu/gkhome/metis/metis/download).

For Linux you can run:

    wget http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz
    gunzip metis-5.1.0.tar.gz
    tar -xvf metis-5.1.0.tar
    cd metis-5.1.0/
    make config shared=1 prefix=<install_path>
    make install

You will probably also need to add this to your environment file:

    export METIS_DLL=/dfs/scratch0/saachi/gurobi/metis_install/lib/libmetis.so

# Running the package
## DataNodes
The main package to track computations is in core.solver. An element which is being tracked is wrapped in a DataNode. A DataNode can be created as: 
    import core.solver as solver
    node = DataNode(3) # a DataNode with data 3
    array_nodes = solver.transform_array(list(range(10))) # a list of DataNodes

DataNodes inter-operate with standard binary operations and most numpy operations. For example, the following program computes the dot product between two vectors:
    import core.solver as solver
    import numpy as np 
    A = np.array(solver.transform_array([1,2]))
    B = np.array(solver.transform_array([3,4]))
    result = np.dot(A, B) # a new DataNode with <A,B>

The result of an operation is automatically wrapped into a new DataNode. Custom operations can also be created via the genop function. For example:
    import core.solver as solver

    A = DataNode(1)
    B = DataNode(2)
    C = DataNode(3)

    def fn(dat):
        return sum(dat)
    
    result = genop([A,B,C], fn)

## Solvers
The bound solvers can also be found in core. The configurations for the bounds can be found in core.state. The methods for each bound can be found in their individual solver files. For example:

## Eigenvalue Solver 
The solver is in eig_solver.py
    from core.eig_solver import compute_eigenvalue_bound

    # M is a list of M values, k is the number of eigenvalues to evaluate
    _, val = compute_eigenvalue_bound(M, k) # compute spectral bound. 


## Partition ILP Solver
The solver is in partition_solver.py in core. Change CHECKPOINT in the solver file to True if checkpointing is desired. The partition size can be found in state.py.
    from core.partition_solver import ILP_BOUND

    S = ILP_BOUND()
    val = S.solve_lb(M, dirname) # lower bound via partitioned ilp
    result, _ = S.solve_ILP(M) # solve exact ILP
    X, val = result 

## Convex Min-Cut Solver and 2S partition solver
The baselines can be found in elango_solver.py.
    from core.elango_solver import get_elango_bound, solve_elango_ilp_bound

    val = get_elango_bound(M) # lower bound for  convex min-cut
    val = solve_elango_ilp_bound(M) # lower bound for elango 2S partition

# Examples 
The computation graphs as well as the tests that appeared in the paper can be found in examples. The plot code can be found in plotting. 