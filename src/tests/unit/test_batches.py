from datetime import date

from src.allocation.domain.model import Batch, OrderLine


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today()),
        OrderLine("order-ref", "SMALL-TABLE", 2)
    )


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("elegant-lamp", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    large_batch, small_line = make_batch_and_line("elegant-lamp", 2, 20)
    assert large_batch.can_allocate(small_line) is False


def test_can_allocate_if_available_equal_to_required():
    large_batch, small_line = make_batch_and_line("elegant-lamp", 2, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "uncomfortable-chair", 100, eta=None)
    different_sku_line = OrderLine("order-123", "expensive-toaster", 10)
    assert batch.can_allocate(different_sku_line) is False