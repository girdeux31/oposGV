
import drivers
from auxiliar import error


class Student:

    def __init__(self, tribunal, name, id):
        """
        PURPOSE:

         Object definition

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         tribunal    Tribunal             Tribunal object
         name        str                  Student name
         id          str                  Student ID
         mark_theory      float                Mark first exam part theory
         mark_practice      float                Mark first exam part problems
         mark_teaching      float                Mark second exam
         mark_total      float                Total mark
        """
        self.name = name
        self.id = id
        self.mark_theory = None
        self.mark_practice = None
        self.mark_teaching = None
        self.mark_total_part_1 = None
        self.mark_total_part_2 = None
        self.passed_part_1 = False
        self.absent_part_1 = True
        self.passed_part_2 = False
        # it is not possible to know absents in part 2, we know passed but not sure if others failed or are absent

        if isinstance(tribunal, drivers.Tribunal):
            self.tribunal = tribunal
            self.tribunal.add_student(self)
        else:
            error(f'Cannot backreference object of type {type(tribunal).__name__}')

        for key in self.tribunal.subject.exam.point_keys:
            setattr(self, key, float())

    def __str__(self):
        """
        PURPOSE:

         Print object

        MANDATORY ARGUMENTS:

         None
        """
        output = str()
        main_keys = ['name', 'id', 'mark_theory', 'mark_practice', 'mark_total_part_1', 'mark_teaching', 'mark_total_part_2', 'passed_part_1', 'absent_part_1', 'passed_part_2']

        for key in main_keys:

            value = getattr(self, key)
            output += '{:s}: {:s}\n'.format(key, str(value))

        for key in self.tribunal.subject.exam.point_keys:

            value = getattr(self, key)

            if value:
                output += '{:s}: {:6.4f}\n'.format(key, value)

        return output
