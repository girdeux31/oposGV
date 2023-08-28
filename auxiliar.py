
import sys
import os
from inspect import stack

# part 3 main mark attributes
point_keys = ['point_t', 'point_1', 'point_2', 'point_3']

# part 3 all mark attributes
# point_keys = ['point_t', 'point_1', 'point_2', 'point_3', 'p11', 'p11a', 'p11b', 'p12', 'p12a', 'p12b', 'p21', 'p22',
#                 'p221', 'p222', 'p223', 'p23', 'p231', 'p232', 'p24', 'p241', 'p242', 'p243', 'p244', 'p245', 'p31',
#                 'p32', 'p321', 'p3211', 'p3212', 'p322', 'p3221', 'p3222', 'p323', 'p33', 'p331', 'p332', 'p333', 'p334',
#                 'p335', 'p336', 'p34', 'p341', 'p342', 'p343', 'p344', 'p345', 'p346', 'p347', 'p348', 'p349', 'p3410',
#                 'p3411', 'p3412', 'p35']

python_version_le_34 = False if sys.version_info[0] >= 3 and sys.version_info[1] > 4 else True

def error(msg, id=None):
    """
    PURPOSE:

     Terminate the program nicely and show the stack table

    MANDATORY ARGUMENTS:

     Parameter   Type                 Definition
     =========== ==================== ==========================================================================================
     logger                           Object returned by start_logger()
     msg         str                  Error message to show through screen

    OPTIONAL ARGUMENTS:

     Parameter   Type                 Default        Definition
     =========== ==================== ============== ===========================================================================
     id          int/None             None           Error ID
    """
    # Write info
    print('')
    print(msg)
    print('')
    print('Traceback is shown, first is the deepest call')
    print('')

    # Write stack table
    print('    {:20s} {:6s} {:20s}'.format('File', 'Line', 'Function'))
    print('    ' + '=' * 20 + ' ' + '=' * 6 + ' ' + '=' * 30)

    for i in range(1, len(stack())):

        if python_version_le_34:
            filename = os.path.basename(stack()[i][1])
            lineno = stack()[i][2]
            function = stack()[i][3]
        else:
            filename = os.path.basename(stack()[i].filename)
            lineno = stack()[i].lineno
            function = stack()[i].function

        print('{:3d} {:20s} {:6d} {:20s}'.format(i, filename, lineno, function))

        if function == 'execfile' or function == '<module>':
            break

    print('')

    if id:
        raise Exception('Fatal error ' + str(id))
    else:
        raise Exception('Fatal error')


def warning(msg, id=None):
    """
    PURPOSE:

     Show nice warning

    MANDATORY ARGUMENTS:

     Parameter   Type                 Definition
     =========== ==================== ==========================================================================================
     msg         str                  Warning message to show through screen

    OPTIONAL ARGUMENTS:

     Parameter   Type                 Default        Definition
     =========== ==================== ============== ===========================================================================
     id          int/None             None           Warning ID
    """
    # Get names
    if python_version_le_34:
        filename = os.path.basename(stack()[1][1])
        lineno = stack()[1][2]
        function = stack()[1][3]
    else:
        filename = os.path.basename(stack()[1].filename)
        lineno = stack()[1].lineno
        function = stack()[1].function

    # Write info
    print('')
    if id:
        print('Warning (' + str(id) + ') in ' + filename + '::' + function + ', line ' + str(lineno))
    else:
        print('Warning in ' + filename + '::' + function + ', line ' + str(lineno))

    print(msg)
    print('')
