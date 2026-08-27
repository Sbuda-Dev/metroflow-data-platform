from storage.processed import ProcessedEventStore

def test_event_is_not_processed_initially(tmp_path):

    store = ProcessedEventStore(base_path=tmp_path)

    assert store.exists("123") is False

def test_event_can_be_marked_as_processed(tmp_path):

    store = ProcessedEventStore(base_path=tmp_path)

    store.mark_processed("123")

    assert store.exists("123") is True