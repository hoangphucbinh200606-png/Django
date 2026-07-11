# onlinecourse/models.py
# (Ensure your other models like Course, Lesson, Enrollment are above this)

class Question(models.Model):
    # Foreign key to lesson
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    # question text
    question_text = models.CharField(max_length=200)
    # question grade/mark
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # Foreign key to question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # choice text
    choice_text = models.CharField(max_length=200)
    # is this choice correct?
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    # Foreign key to enrollment
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    # Many-to-many relationship with Choice
    choices = models.ManyToManyField(Choice)
