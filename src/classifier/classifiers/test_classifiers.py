from models import Verdict


def is_negative(verdict: Verdict) -> bool:
    return verdict.negative and verdict.negative > 0.2


def is_positive(verdict: Verdict) -> bool:
    return verdict.positive and verdict.positive > 0.2


def is_neutral(verdict: Verdict) -> bool:
    return verdict.neutral and verdict.neutral > 0.8

