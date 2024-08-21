# from django.test import TestCase
# # Import the Lesson model
# from lessons.models import Lesson

# # The lesson model should have the following fields: Date, Time, Duration, StudentID, ApprovalID, RequestApproval, Instrument, TeacherID, and InvoiceReference
# # Request approval should be a boolean field
# # StudentID, ApprovalID, TeacherID, and InvoiceReference should be foreign keys
# # Date and Time should be DateTime fields
# # Duration should be an integer field (minutes)
# # Instrument should be a CharField with a max length of 50
# # Date, Time and StudentID should be unique together
# # Date, Time and TeacherID should be unique together
>>>>>>>>> Temporary merge branch 2


# class LessonTestCase(TestCase):
#     def setUp(self):
#         Lesson.objects.create(Date="2020-01-01", Time="12:00", Duration="60", StudentID="1", ApprovalID="1", RequestApproval="true", Instrument="Guitar", TeacherID="1", InvoiceReference="1")

#     def test_lesson_date(self):
#         lesson = Lesson.objects.get(Date="2020-01-01")
#         self.assertEqual(lesson.Date, "2020-01-01")

#     def test_lesson_time(self):
#         lesson = Lesson.objects.get(Time="12:00")
#         self.assertEqual(lesson.Time, "12:00")

#     def test_lesson_duration(self):
#         lesson = Lesson.objects.get(Duration="1:00")
#         self.assertEqual(lesson.Duration, "60")

#     def test_lesson_studentid(self):
#         lesson = Lesson.objects.get(StudentID="1")
#         self.assertEqual(lesson.StudentID, "1")

#     def test_lesson_approvalid(self):
#         lesson = Lesson.objects.get(ApprovalID="1")
#         self.assertEqual(lesson.ApprovalID, "1")

#     def test_lesson_requestapproval(self):
#         lesson = Lesson.objects.get(RequestApproval="true")
#         self.assertEqual(lesson.RequestApproval, "true")

#     def test_lesson_instrument(self):
#         lesson = Lesson.objects.get(Instrument="1")
#         self.assertEqual(lesson.Instrument, "1")

#     def test_lesson_teacherid(self):
#         lesson = Lesson.objects.get(TeacherID="1")
#         self.assertEqual(lesson.TeacherID, "1")

#     def test_lesson_invoicereference(self):
#         lesson = Lesson.objects.get(InvoiceReference="1")
#         self.assertEqual(lesson.InvoiceReference, "1")

#     def test_lesson_date_time_studentid(self):
#         lesson = Lesson.objects.get(Date="2020-01-01", Time="12:00", StudentID="1")
#         self.assertEqual(lesson.Date, "2020-01-01")
#         self.assertEqual(lesson.Time, "12:00")
#         self.assertEqual(lesson.StudentID, "1")

#     def test_lesson_date_time_teacherid(self):
#         lesson = Lesson.objects.get(Date="2020-01-01", Time="12:00", TeacherID="1")
#         self.assertEqual(lesson.Date, "2020-01-01")
#         self.assertEqual(lesson.Time, "12:00")
#         self.assertEqual(lesson.TeacherID, "1")

        

