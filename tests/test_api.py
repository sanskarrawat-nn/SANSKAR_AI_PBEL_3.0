import unittest
import requests

BASE_URL = "http://127.0.0.1:8000"

class TestElearningAPI(unittest.TestCase):
    def setUp(self):
        # Reset progress before tests to have a deterministic state
        try:
            requests.post(f"{BASE_URL}/api/v1/progress/reset")
        except requests.exceptions.ConnectionError:
            pass

    def test_1_get_course_details(self):
        """Test GET /api/v1/course/{course_id} returns correct structure and modules."""
        url = f"{BASE_URL}/api/v1/course/1"
        try:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["Course_ID"], "1")
            self.assertEqual(data["Title"], "Java Beginners Tutorial")
            self.assertIn("modules", data)
            self.assertEqual(len(data["modules"]), 3)
            
            # Module 1 should be unlocked, Module 2 and 3 should be locked
            m1 = data["modules"][0]
            m2 = data["modules"][1]
            self.assertEqual(m1["Module_Order"], 1)
            self.assertFalse(m1["is_locked"])
            self.assertEqual(m2["Module_Order"], 2)
            self.assertTrue(m2["is_locked"])
            print("\n[PASS] Course details retrieval and lock state validation.")
        except requests.exceptions.ConnectionError:
            self.fail("Server is offline. Start the backend before running tests.")

    def test_2_verify_correct_answer_normalization(self):
        """Test POST /api/v1/module/verify with correct normalized and unnormalized answers."""
        url = f"{BASE_URL}/api/v1/module/verify"
        
        # Test exact match
        payload = {
            "course_id": "1",
            "module_id": "1_1",
            "user_answer": "System.out.print('Hello');"
        }
        try:
            r = requests.post(url, json=payload)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertTrue(data["success"])
            self.assertTrue(data["unlocked_next"])
            
            # Reset progress again
            requests.post(f"{BASE_URL}/api/v1/progress/reset")
            
            # Test unnormalized match (whitespaces and quotes differences)
            payload_unnormalized = {
                "course_id": "1",
                "module_id": "1_1",
                "user_answer": "  System.out.print( \"Hello\" ) ;  "
            }
            r = requests.post(url, json=payload_unnormalized)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertTrue(data["success"])
            self.assertTrue(data["unlocked_next"])
            print("[PASS] Module verification with normalization.")
        except requests.exceptions.ConnectionError:
            self.fail("Server is offline.")

    def test_3_verify_incorrect_answer(self):
        """Test POST /api/v1/module/verify with garbage answer fails defensively."""
        url = f"{BASE_URL}/api/v1/module/verify"
        payload = {
            "course_id": "1",
            "module_id": "1_1",
            "user_answer": "System.out.println('Hello')"
        }
        try:
            r = requests.post(url, json=payload)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertFalse(data["success"])
            self.assertFalse(data["unlocked_next"])
            print("[PASS] Module verification with incorrect answer.")
        except requests.exceptions.ConnectionError:
            self.fail("Server is offline.")

    def test_4_locked_module_submission(self):
        """Test that submitting answer for a locked module returns 403."""
        url = f"{BASE_URL}/api/v1/module/verify"
        # Module 1_2 is locked initially
        payload = {
            "course_id": "1",
            "module_id": "1_2",
            "user_answer": "int age = 20;"
        }
        try:
            r = requests.post(url, json=payload)
            self.assertEqual(r.status_code, 403)
            print("[PASS] Defensive checking for locked module submission.")
        except requests.exceptions.ConnectionError:
            self.fail("Server is offline.")

if __name__ == "__main__":
    unittest.main()
