from typing import Any, Iterator, Optional, Union, Generator


class HashTable:
    """A hash table implementation with chaining collision resolution.
    
    Features automatic resizing, load factor tracking, and dictionary-like interface.
    
    Attributes:
        size: Current capacity of the hash table
        load_factor: Ratio of items to capacity (0.0 to 1.0)
    """
    
    def __init__(self, size: int = 2**4) -> None:
        """Initialize a new hash table.
        
        Args:
            size: Initial capacity of the hash table. Must be positive.
        """
        self.size = size
        self.__table: list[list[tuple[Any, Any]]] = [[] for _ in range(size)]

    def _hash(self, key: Any) -> int:
        """Compute CRC32-like hash value for the given key.
        
        Args:
            key: Key to hash. Will be converted to string.
            
        Returns:
            Integer hash value.
        """
        hash_value = 0
        for char in str(key):
            hash_value ^= ord(char)
            hash_value = (hash_value << 1) | (hash_value >> 31)
        return hash_value

    def _hash_index(self, key: Any) -> int:
        """Compute bucket index for the given key.
        
        Args:
            key: Key to locate bucket for.
            
        Returns:
            Index in the table array.
        """
        hash_value: int = self._hash(key)
        return abs(hash_value) % self.size

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve value associated with key.
        
        Args:
            key: Key to search for.
            
        Returns:
            Associated value if found, None otherwise.
        """
        hash_index: int = self._hash_index(key)
        bucket: list[tuple[Any, Any]] = self.__table[hash_index]

        for stored_key, stored_value in bucket:
            if stored_key == key:
                return stored_value
        return None

    def put(self, key: Any, value: Any) -> int:
        """Insert or update a key-value pair.
        
        Args:
            key: Key to insert/update.
            value: Value to associate with key.
            
        Returns:
            Index where the pair was stored.
            
        Raises:
            TypeError: If key is not hashable.
        """
        if self.need_resize:
            self._resize(self.size * 2)

        hash_index: int = self._hash_index(key)
        bucket: list[tuple[Any, Any]] = self.__table[hash_index]

        for i, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket[i] = (key, value)
                return hash_index

        bucket.append((key, value))
        return hash_index

    def delete(self, key: Any) -> bool:
        """Remove key-value pair from hash table.
        
        Args:
            key: Key to remove.
            
        Returns:
            True if key was found and removed, False otherwise.
        """
        hash_index: int = self._hash_index(key)
        bucket: list[tuple[Any, Any]] = self.__table[hash_index]

        for i, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                del bucket[i]
                
                # Check if we need to shrink after deletion
                if self.load_factor < 0.2 and self.size > 16:
                    self._resize(self.size // 2)
                return True
        return False

    def _resize(self, new_size: int) -> None:
        """Resize hash table and rehash all elements.
        
        Args:
            new_size: New capacity for the hash table.
            
        Raises:
            ValueError: If new_size is not positive.
        """
        if new_size <= 0:
            raise ValueError("Hash table size must be positive")
            
        old_table = self.__table
        self.size = new_size
        self.__table = [[] for _ in range(self.size)]
        
        for bucket in old_table:
            for key, value in bucket:
                self.put(key, value)

    @property
    def load_factor(self) -> float:
        """Calculate current load factor (items / capacity).
        
        Returns:
            Current load factor rounded to 2 decimal places.
        """
        total_items = sum(len(bucket) for bucket in self.__table)
        return round(total_items / self.size, 2)

    @property
    def need_resize(self) -> bool:
        """Check if hash table needs resizing.
        
        Returns:
            True if load factor exceeds 0.7, False otherwise.
        """
        return self.load_factor > 0.7

    def get_collisions_count(self) -> int:
        """Count number of buckets with collisions.
        
        Returns:
            Number of buckets containing more than one item.
        """
        return sum(1 for bucket in self.__table if len(bucket) > 1)

    def items(self) -> Iterator[tuple[Any, Any]]:
        """Iterate over all key-value pairs.
        
        Yields:
            Tuples of (key, value) pairs.
        """
        for bucket in self.__table:
            for key, value in bucket:
                yield key, value

    def keys(self) -> list[Any]:
        """Get all keys in hash table.
        
        Returns:
            List of all keys.
        """
        return [key for bucket in self.__table for key, _ in bucket]

    def values(self) -> list[Any]:
        """Get all values in hash table.
        
        Returns:
            List of all values.
        """
        return [value for bucket in self.__table for _, value in bucket]

    def to_dict(self) -> dict[Any, Any]:
        """Convert hash table to dictionary.
        
        Returns:
            Dictionary containing all key-value pairs.
        """
        return dict(self.items())

    @classmethod
    def from_dict(cls, data: dict[Any, Any], size: Optional[int] = None) -> 'HashTable':
        """Create hash table from dictionary.
        
        Args:
            data: Dictionary to convert to hash table.
            size: Optional initial size. Uses dict length if not specified.
            
        Returns:
            New HashTable instance.
        """
        hashtable = cls(size or len(data))
        for key, value in data.items():
            hashtable.put(key, value)
        return hashtable

    def __contains__(self, key: Any) -> bool:
        """Check if key exists in hash table.
        
        Args:
            key: Key to check.
            
        Returns:
            True if key exists, False otherwise.
        """
        return key in [_key for bucket in self.__table for _key, _ in bucket]

    def __str__(self) -> str:
        """String representation of hash table.
        
        Returns:
            String showing internal table structure.
        """
        return str(self.__table)

    def __iter__(self) -> Iterator[Any]:
        """Iterate over keys in hash table.
        
        Yields:
            Each key in the hash table.
        """
        for bucket in self.__table:
            for key, _ in bucket:
                yield key

    def __getitem__(self, key: Any) -> Any:
        """Get value using subscript notation.
        
        Args:
            key: Key to look up.
            
        Returns:
            Value associated with key.
            
        Raises:
            KeyError: If key not found.
        """
        value = self.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")
        return value

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set value using subscript notation.
        
        Args:
            key: Key to set.
            value: Value to associate with key.
        """
        self.put(key, value)

    def __delitem__(self, key: Any) -> None:
        """Delete key using del statement.
        
        Args:
            key: Key to delete.
            
        Raises:
            KeyError: If key not found.
        """
        if not self.delete(key):
            raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        """Get number of items in hash table.
        
        Returns:
            Total number of key-value pairs.
        """
        return sum(len(bucket) for bucket in self.__table)
      
