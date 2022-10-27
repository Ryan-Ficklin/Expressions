import unittest
from stack_array import Stack
        
class TestLab2(unittest.TestCase):

    def test_init(self) -> None:
        stack = Stack(5)
        self.assertEqual(stack.items, [None]*5)
        self.assertEqual(stack.capacity, 5)

        stack = Stack(5, [1, 2])
        self.assertEqual(stack.items[0:2], [1, 2])
        self.assertEqual(stack.capacity, 5)

        with self.assertRaises(IndexError):
            Stack(5, [1, 2, 3, 4, 5, 6])

    def test_eq(self) -> None:
        stack1 = Stack(5)
        stack2 = Stack(5)
        stack3 = Stack(10)
        stack4 = Stack(5,[1, 2])
        self.assertEqual(stack1, stack2)
        self.assertNotEqual(stack1, stack3)
        self.assertNotEqual(stack1, stack4)
        self.assertFalse(stack1.__eq__(None))

    def test_repr(self) -> None:
        stack = Stack(5, [1, 2])
        self.assertEqual(stack.__repr__(), "Stack(5, [1, 2])")

# WRITE TESTS FOR STACK OPERATIONS - PUSH, POP, PEEK, etc.
    def test_push(self) -> None:
        stack = Stack(5, [])
        stack.push(1)
        self.assertEqual(stack, Stack(5, [1]))
        stack.push(2)
        self.assertEqual(stack, Stack(5, [1, 2]))

    def test_full_push(self) -> None:
        stack = Stack(3, [1, 2])
        stack.push(4)
        with self.assertRaises(IndexError):
            stack.push(5)

    def test_pop(self) -> None:
        stack = Stack(5, [1, 2, 3, 4, 5])
        self.assertEqual(stack.pop(), 5)
        self.assertEqual(stack, Stack(5, [1, 2, 3, 4]))

    def test_empty_pop(self) -> None:
        stack = Stack(5, [1, 2])
        stack.pop()
        stack.pop()
        with self.assertRaises(IndexError):
            stack.pop()

    def test_last_in_first_out(self) -> None:
        stack = Stack(5, [])
        stack.push(3)
        stack.push(2)
        self.assertEqual(stack, Stack(5, [3, 2]))
        stack.pop()
        self.assertEqual(stack, Stack(5, [3]))

    def test_is_empty(self) -> None:
        stack1 = Stack(1)
        self.assertTrue(stack1.is_empty())
        stack2 = Stack(5, [1, 2, 3, 4, 5])
        while stack2.size() > 0:
            stack2.pop()
        self.assertTrue(stack2.is_empty())

    def test_is_full(self) -> None:
        stack1 = Stack(0)
        # interesting I suppose
        self.assertTrue(stack1.is_full())
        self.assertTrue(stack1.is_empty())
        stack2 = Stack(2, [1])
        stack2.push(12)
        self.assertTrue(stack2.is_full())

    def test_peek(self) -> None:
        stack1 = Stack(4, [1,2])
        self.assertEqual(stack1.peek(), 2)
        stack1.push(4)
        stack1.push(15)
        self.assertEqual(stack1.peek(), 15)
        stack1.pop()
        self.assertEqual(stack1.peek(), 4)

    def test_peek_empty(self) -> None:
        stack1 = Stack(3, [])
        with self.assertRaises(IndexError):
            stack1.peek()
        stack2 = Stack(0)
        with self.assertRaises(IndexError):
            stack2.peek()

    def test_size(self) -> None:
        stack1 = Stack(5, [1, 2, 3, 4])
        self.assertEqual(stack1.size(), 4)
        stack2 = Stack(0)
        self.assertEqual(stack2.size(), 0)
        stack1.push(16)
        self.assertEqual(stack1.size(), 5)
        stack1.pop()
        stack1.pop()
        self.assertEqual(stack1.size(), 3)

    def test_works_with_not_int(self) -> None:
        stack = Stack(5, ["str", 11.5, 4])
        stack.push("")
        self.assertEqual(stack, Stack(5, ["str", 11.5, 4, ""]))
        stack.pop()
        stack.pop()
        self.assertEqual(stack, Stack(5, ["str", 11.5]))

if __name__ == '__main__': 
    unittest.main()
