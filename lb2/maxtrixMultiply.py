from mpi4py import MPI
from random import randint
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
workers = comm.Get_size()

mtrx1 = []
mtrx2 = []
mtrx3 = []

N = 2


def init_matrix():
    """
    Initialize matrix from here, we do initialize three matrix from here
        1. mtrx1 - input matrix
        2. mtrx2 - input matrix
        3. mtrx3 - output matrix
    """
    global mtrx1
    mtrx1 = [[randint(0, 10) for i in range(N)] for j in range(N)]

    global mtrx2
    mtrx2 = [[randint(0, 10) for i in range(N)] for j in range(N)]


def multiply_matrix(X, Y):
    """
    Generate new matrix by multiplying incoming matrix data.
    This function will be called by each and every slave with their matrix
    data. For an example
    X = [
            [1, 2, 3, 4],
            [3, 2, 3, 7],
        ]
    Y = [
            [1, 2, 3],
            [5, 6, 7],
            [2, 2, 7],
            [5, 6, 9],
        ]
    Z = [
            [(1*1 + 2*5 + 3*2 + 4*5), (1*2 + 2*6 + 3*2 + 4*6), --, --],
            [(3*1 + 2*5 + 3*2 + 7*5), (3*2 + 2*6 + 3*2 + 7*6), --, --]
        ]
    Args:
        X: rows of mtrx1
        Y: whole mtrx2
    Returns:
        Z: calculated matrix part
    """
    Z = [[sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)]
            for X_row in X]

    return Z


def distribute_matrix_data():
    """
    Distribute rows of first matrix and whole second matrix to salves, this
    done via master node. Then salves calculate a sub matrix by multiplying
    incoming matrix and send result back to master
    """
    def split_matrix(seq, p):
        """
        Split matrix into small parts according to the no of workers. These
        parts will be send to slaves by master node
        """
        rows = []
        n = int(len(seq) / p)
        r = len(seq) % p
        b, e = 0, n + min(1, r)
        for i in range(p):
            print(b, " =============================", e)
            rows.append(seq[b:e])
            r = max(0, r - 1)
            b, e = e, e + n + min(1, r) 

        return rows

    rows = split_matrix(mtrx1, workers)

    pid = 1
    for row in rows:
        comm.send(row, dest=pid, tag=1)
        comm.send(mtrx2, dest=pid, tag=2)
        pid = pid + 1


def assemble_matrix_data():
    """
    Assemble returning values form salves and generate final matrix. Slaves
    calculate single rows of final matrix
    """
    global mtrx3

    pid = 1
    for n in range(workers):
        row = comm.recv(source=pid, tag=pid)
        mtrx3 = mtrx3 + row
        pid = pid + 1


def master_operation():
    """
    Do operation of master node, we have to do following this from here
        1. distribute matrix data to slaves
        2. assemble salves returning values and generate final matrix
    """
    distribute_matrix_data()
    assemble_matrix_data()


def slave_operation():
    """
    Do operation of slave nodes, we have to do
        1. Gather the data sending from master
        2. Calculate the single fow of final matrix
        3. Send the calculated row back to master
    """
    # receive data from master node
    x = comm.recv(source=0, tag=1)
    y = comm.recv(source=0, tag=2)

    # multiply the received matrix and send the result back to master
    z = multiply_matrix(x, y)
    comm.send(z, dest=0, tag=rank)


if __name__ == '__main__':
    """
    Main method here, we have to do
        1. initialize matrix
        2. Master/Salve operations
    """
    if rank == 0:
        init_matrix()

        # start time
        t1 = time.time()
        print('--------------------------------------------------------------')
        print('Start time', t1)
        print('--------------------------------------------------------------')
        print('\n')

        master_operation()

        # end time
        t2 = time.time()

        print('--------------------------------------------------------------')
        print(mtrx1)
        print('--------------------------------------------------------------')
        print('\n')

        print('--------------------------------------------------------------')
        print(mtrx2)
        print('--------------------------------------------------------------')
        print('\n')

        print('--------------------------------------------------------------')
        print(mtrx3)
        print('--------------------------------------------------------------')
        print('\n')

        print('--------------------------------------------------------------')
        print('Start time', t1)
        print('--------------------------------------------------------------')
        print('\n')

        print('--------------------------------------------------------------')
        print('End time', t2)
        print('--------------------------------------------------------------')
        print('\n')

        print('--------------------------------------------------------------')
        print('Time taken in seconds', int(t2 - t1))
        print('--------------------------------------------------------------')
        print('\n')
    else:
        slave_operation()   