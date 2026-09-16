# Debug Lab Answers: Module 21

<details>
<summary>Bug 1: Descriptor storing state on self instead of instance</summary>

### Root Cause
Descriptor objects live on the class dictionary, meaning there is only one descriptor instance shared across all instances of the owner class. Storing `self.val` treats all instances as identical.

### Fix
Use `__set_name__` to record the attribute name, and store the value on the target instance:
```python
class CorrectDescriptor:
    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)
```
</details>
