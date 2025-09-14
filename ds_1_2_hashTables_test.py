import pytest
from ds_1_2_hashTables import HashTable


class TestHashTable:
    """Тесты для класса HashTable"""

    def test_initialization(self):
        """Тест инициализации хэш-таблицы"""
        ht = HashTable()
        assert ht.size == 16  # 2^4 по умолчанию
        assert len(ht) == 0
        assert ht.load_factor == 0.0

    def test_custom_initial_size(self):
        """Тест инициализации с пользовательским размером"""
        ht = HashTable(size=8)
        assert ht.size == 8
        assert len(ht) == 0

    def test_put_and_get(self):
        """Тест добавления и получения элементов"""
        ht = HashTable()
        ht.put("key1", "value1")
        ht.put("key2", 42)
        ht.put(123, [1, 2, 3])
        
        assert ht.get("key1") == "value1"
        assert ht.get("key2") == 42
        assert ht.get(123) == [1, 2, 3]
        assert ht.get("nonexistent") is None

    def test_subscript_access(self):
        """Тест доступа через квадратные скобки"""
        ht = HashTable()
        ht["key1"] = "value1"
        ht["key2"] = "value2"
        
        assert ht["key1"] == "value1"
        assert ht["key2"] == "value2"
        
        with pytest.raises(KeyError):
            _ = ht["nonexistent"]

    def test_subscript_assignment(self):
        """Тест присваивания через квадратные скобки"""
        ht = HashTable()
        ht["test"] = "value"
        assert ht["test"] == "value"
        
        # Обновление значения
        ht["test"] = "new_value"
        assert ht["test"] == "new_value"

    def test_delete(self):
        """Тест удаления элементов"""
        ht = HashTable()
        ht.put("key1", "value1")
        ht.put("key2", "value2")
        
        assert ht.delete("key1") is True
        assert ht.get("key1") is None
        assert len(ht) == 1
        
        assert ht.delete("nonexistent") is False

    def test_del_statement(self):
        """Тест использования del"""
        ht = HashTable()
        ht["key1"] = "value1"
        ht["key2"] = "value2"
        
        del ht["key1"]
        assert "key1" not in ht
        assert len(ht) == 1
        
        with pytest.raises(KeyError):
            del ht["nonexistent"]

    def test_contains(self):
        """Тест оператора in"""
        ht = HashTable()
        ht["key1"] = "value1"
        
        assert "key1" in ht
        assert "nonexistent" not in ht

    def test_len(self):
        """Тест получения длины"""
        ht = HashTable()
        assert len(ht) == 0
        
        for i in range(5):
            ht.put(f"key{i}", f"value{i}")
        
        assert len(ht) == 5
        
        ht.delete("key0")
        assert len(ht) == 4

    def test_load_factor_calculation(self):
        """Тест вычисления коэффициента загрузки"""
        ht = HashTable(size=4)  # Маленький размер для теста
        
        assert ht.load_factor == 0.0
        
        ht.put("key1", "value1")
        assert ht.load_factor == 0.25  # 1/4
        
        ht.put("key2", "value2")
        assert ht.load_factor == 0.50  # 2/4
        
        ht.put("key3", "value3")
        assert ht.load_factor == 0.75  # 3/4

    def test_auto_resize_on_put(self):
        """Тест автоматического увеличения размера"""
        ht = HashTable(size=4)  # Маленький начальный размер
        
        # Добавляем элементы до превышения порога
        for i in range(3):  # 3/4 = 0.75 (еще не превышает)
            ht.put(f"key{i}", f"value{i}")
        
        original_size = ht.size
        
        # Добавляем еще один элемент, должен вызвать resize
        ht.put("trigger", "resize")
        
        assert ht.size > original_size
        assert ht.load_factor < 0.7  # Должен быть сброшен после resize

    def test_auto_resize_on_delete(self):
        """Тест автоматического уменьшения размера"""
        ht = HashTable(size=32)  # Большой начальный размер
        
        # Добавляем много элементов
        for i in range(25):  # 25/32 ≈ 0.78
            ht.put(f"key{i}", f"value{i}")
        
        # Удаляем большинство элементов
        for i in range(20):  # Остается 5/32 ≈ 0.15
            ht.delete(f"key{i}")
        
        # Должен произойти resize в меньшую сторону
        assert ht.size < 32
        assert ht.load_factor > 0.15  # Но не слишком маленький

    def test_collision_handling(self):
        """Тест обработки коллизий"""
        ht = HashTable(size=2)  # Очень маленький размер для принудительных коллизий
        
        # Добавляем элементы, которые скорее всего вызовут коллизии
        ht.put("a", 1)
        ht.put("b", 2) 
        ht.put("c", 3)
        
        assert len(ht) == 3
        assert ht.get_collisions_count() > 0  # Должны быть коллизии
        
        # Проверяем, что все значения доступны несмотря на коллизии
        assert ht.get("a") == 1
        assert ht.get("b") == 2
        assert ht.get("c") == 3

    def test_items_iterator(self):
        """Тест итератора по элементам"""
        ht = HashTable()
        test_data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        
        for key, value in test_data.items():
            ht.put(key, value)
        
        items = list(ht.items())
        assert len(items) == 3
        assert set(items) == set(test_data.items())

    def test_keys_and_values(self):
        """Тест методов keys() и values()"""
        ht = HashTable()
        test_data = {"key1": "value1", "key2": "value2"}
        
        for key, value in test_data.items():
            ht.put(key, value)
        
        assert set(ht.keys()) == set(test_data.keys())
        assert set(ht.values()) == set(test_data.values())

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        ht = HashTable()
        test_data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        
        for key, value in test_data.items():
            ht.put(key, value)
        
        result_dict = ht.to_dict()
        assert result_dict == test_data

    def test_from_dict_classmethod(self):
        """Тест создания из словаря"""
        test_data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        ht = HashTable.from_dict(test_data)
        
        assert len(ht) == 3
        for key, value in test_data.items():
            assert ht.get(key) == value

    def test_from_dict_with_custom_size(self):
        """Тест создания из словаря с пользовательским размером"""
        test_data = {"key1": "value1", "key2": "value2"}
        ht = HashTable.from_dict(test_data, size=10)
        
        assert ht.size == 10
        assert len(ht) == 2

    def test_iteration(self):
        """Тест итерации по ключам"""
        ht = HashTable()
        test_keys = ["key1", "key2", "key3"]
        
        for key in test_keys:
            ht.put(key, "value")
        
        iterated_keys = list(ht)
        assert set(iterated_keys) == set(test_keys)

    def test_string_representation(self):
        """Тест строкового представления"""
        ht = HashTable()
        ht.put("test", "value")
        
        representation = str(ht)
        assert isinstance(representation, str)
        assert "test" in representation or "value" in representation

    def test_hash_consistency(self):
        """Тест консистентности хэш-функции"""
        ht = HashTable()
        
        # Один и тот же ключ должен всегда давать одинаковый хэш
        hash1 = ht._hash("test_key")
        hash2 = ht._hash("test_key")
        assert hash1 == hash2
        
        # Разные ключи должны давать разные хэши (в большинстве случаев)
        hash3 = ht._hash("different_key")
        assert hash1 != hash3

    def test_hash_index_range(self):
        """Тест что индекс хэша всегда в допустимом диапазоне"""
        ht = HashTable(size=10)
        
        test_keys = ["a", "b", "c", "long_key_name", 123, 45.67, None, [1, 2, 3]]
        
        for key in test_keys:
            index = ht._hash_index(key)
            assert 0 <= index < ht.size

    def test_update_existing_key(self):
        """Тест обновления существующего ключа"""
        ht = HashTable()
        ht.put("key", "old_value")
        assert ht.get("key") == "old_value"
        
        ht.put("key", "new_value")
        assert ht.get("key") == "new_value"
        assert len(ht) == 1  # Всего один элемент

    def test_clear_table_with_deletion(self):
        """Тест полной очистки таблицы"""
        ht = HashTable()
        
        # Добавляем элементы
        for i in range(10):
            ht.put(f"key{i}", f"value{i}")
        
        assert len(ht) == 10
        
        # Удаляем все элементы
        for i in range(10):
            ht.delete(f"key{i}")
        
        assert len(ht) == 0
        assert ht.load_factor == 0.0

    def test_various_key_types(self):
        """Тест различных типов ключей"""
        ht = HashTable()
        
        test_cases = [
            ("string", "value1"),
            (123, "value2"),
            (45.67, "value3"),
            (None, "value4"),
            (True, "value5"),
            ((1, 2), "value6"),
            (frozenset([1, 2]), "value7")
        ]
        
        for key, value in test_cases:
            ht.put(key, value)
            assert ht.get(key) == value

    def test_none_values(self):
        """Тест хранения None в качестве значения"""
        ht = HashTable()
        ht.put("key", None)
        assert ht.get("key") is None
        assert "key" in ht

    def test_large_number_of_elements(self):
        """Тест с большим количеством элементов"""
        ht = HashTable()
        
        # Добавляем много элементов
        for i in range(1000):
            ht.put(f"key{i}", f"value{i}")
        
        assert len(ht) == 1000
        assert ht.load_factor <= 0.7  # Должен быть автоматически отресайзен
        
        # Проверяем доступ ко всем элементам
        for i in range(1000):
            assert ht.get(f"key{i}") == f"value{i}"

    def test_resize_validation(self):
        """Тест валидации размера при resize"""
        ht = HashTable()
        
        with pytest.raises(ValueError, match="Hash table size must be positive"):
            ht._resize(0)
        
        with pytest.raises(ValueError, match="Hash table size must be positive"):
            ht._resize(-5)

