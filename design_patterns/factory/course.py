from abc import ABC, abstractmethod


# Create a base class for Modules

class Module(ABC):
    @abstractmethod
    def get_module_name(self):
        pass

    @abstractmethod
    def get_duration(self):
        pass

# Concrete module classes for different types of modules

class UMLBasics(Module):
    def get_module_name(self):
        return "UML Basics"

    def get_duration(self):
        return "2 weeks"

class DesignPatterns(Module):
    def get_module_name(self):
        return "Design Patterns"

    def get_duration(self):
        return "3 weeks"

class SystemComponents(Module):
    def get_module_name(self):
        return "System Components"

    def get_duration(self):
        return "4 weeks"

class ScalableSystems(Module):
    def get_module_name(self):
        return "Scalable Systems"

    def get_duration(self):
        return "5 weeks"

class SortingAlgorithms(Module):
    def get_module_name(self):
        return "Sorting Algorithms"

    def get_duration(self):
        return "1 week"

class GraphAlgorithms(Module):
    def get_module_name(self):
        return "Graph Algorithms"

    def get_duration(self):
        return "3 weeks"   


# Create a base class for Course

class Course(ABC):
    @abstractmethod
    def get_course_name(self):
        pass

    @abstractmethod
    def get_modules(self):
        pass


# Create concrete classes for each course
class LLDCourse(Course):
    def get_course_name(self):
        return "Low-Level Design (LLD)"

    def get_modules(self):
        return [UMLBasics(), DesignPatterns()]

class HLDCourse(Course):
    def get_course_name(self):
        return "High-Level Design (HLD)"

    def get_modules(self):
        return [SystemComponents(), ScalableSystems()]

class DSACourse(Course):
    def get_course_name(self):
        return "Data Structures and Algorithms (DSA)"

    def get_modules(self):
        return [SortingAlgorithms(), GraphAlgorithms()]


# Create a Course Factory
class CourseFactory:
    @staticmethod
    def create_course(course_type) -> Course:
        if course_type == "LLD":
            return LLDCourse()
        elif course_type == "HLD":
            return HLDCourse()
        elif course_type == "DSA":
            return DSACourse()
        else:
            raise ValueError(f"Unknown course type: {course_type}")


# Use the factory to create courses and display details


if __name__ == "__main__":
    # Course types to create
    course_types = ["LLD", "HLD", "DSA", "AI"]

    for course_type in course_types:
        try:
            course = CourseFactory.create_course(course_type)
            print(f"Course: {course.get_course_name()}")
            print("Modules:")
            for module in course.get_modules():
                print(f"  - {module.get_module_name()} ({module.get_duration()})")
            print()
        except ValueError as e:
            print(e)

 
