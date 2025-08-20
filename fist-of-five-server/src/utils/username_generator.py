import random
import re
from dataclasses import dataclass
from typing import Iterable, Sequence

# No digits, lowercase, dot-separated tokens
USERNAME_MAX_LEN = 126
TOKEN_SEP = "."

# small curated banks; you can add/replace at runtime
ADJECTIVES: Sequence[str] = (
    "mighty", "silent", "arcane", "wandering", "stark",
    "wild", "rogue", "valiant", "lone", "scarlet",
    "grim", "iron", "golden", "shadow", "stormborn",
)
PERSONAS: Sequence[str] = (
    "wizard", "witcher", "ranger", "paladin", "knight",
    "archer", "samurai", "ronin", "assassin", "alchemist",
    "guardian", "vanguard", "sorcerer", "bard", "druid",
)
REALMS: Sequence[str] = (
    "winterfell", "gotham", "asgard", "wakanda", "hogwarts",
    "mordor", "rivendell", "night.city", "camelot", "pandora",
)
FRANCHISE: Sequence[str] = (
    "dark.knight", "stranger.things", "the.witcher", "last.of.us",
    "house.of.dragons", "game.of.thrones", "breaking.bad",
)

# connectors to make it read like English but still dotty
CONNECTORS: Sequence[str] = ("of", "from", "the", "with")

# patterns are tuples of token-choices; generator picks one randomly
PATTERNS: Sequence[Sequence[str]] = (
    ("ADJ", "PERSONA"),
    ("ADJ", "PERSONA", "of", "REALM"),
    ("PERSONA", "from", "REALM"),
    ("ADJ", "FRANCHISE"),
    ("ADJ", "PERSONA", "the", "ADJ"),
)

@dataclass(frozen=True)
class UsernameSeed:
    # Feed in whatever you like (uid, names) to make the RNG deterministic per user
    uid: str
    first_name: str | None = None
    last_name: str | None = None

class UsernameGenerator:
    def __init__(
        self,
        adjectives: Sequence[str] = ADJECTIVES,
        personas: Sequence[str] = PERSONAS,
        realms: Sequence[str] = REALMS,
        franchises: Sequence[str] = FRANCHISE,
        connectors: Sequence[str] = CONNECTORS,
        patterns: Sequence[Sequence[str]] = PATTERNS,
    ):
        self.adj = tuple(self._clean_bank(adjectives))
        self.per = tuple(self._clean_bank(personas))
        self.rlm = tuple(self._clean_bank(realms))
        self.frc = tuple(self._clean_bank(franchises))
        self.con = tuple(connectors)
        self.patterns = tuple(patterns)

    def _clean_bank(self, items: Iterable[str]) -> list[str]:
        out: list[str] = []
        for s in items:
            s = s.strip().lower()
            s = re.sub(r"[^a-z.]+", ".", s)  # enforce a–z and dots only
            s = re.sub(r"\.{2,}", ".", s).strip(".")
            if s and not re.search(r"\d", s):
                out.append(s)
        return out

    def _pick(self, rng: random.Random, label: str) -> str:
        if label == "ADJ": return rng.choice(self.adj)
        if label == "PERSONA": return rng.choice(self.per)
        if label == "REALM": return rng.choice(self.rlm)
        if label == "FRANCHISE": return rng.choice(self.frc)
        # connector literal like "of"/"the"/"from"
        return label

    def propose(self, seed: UsernameSeed, *, attempt: int = 0) -> str:
        # deterministic but varied RNG per user+attempt
        h = f"{seed.uid}::{seed.first_name or ''}::{seed.last_name or ''}::{attempt}"
        rng = random.Random()
        rng.seed(h)

        pattern = rng.choice(self.patterns)
        tokens = [self._pick(rng, t) for t in pattern]
        # occasionally stitch in the first or last name (cleaned), still no digits
        if seed.first_name and rng.random() < 0.3:
            tokens.insert(0, re.sub(r"[^a-z]+", ".", seed.first_name.lower()).strip("."))
        if seed.last_name and rng.random() < 0.2:
            tokens.append(re.sub(r"[^a-z]+", ".", seed.last_name.lower()).strip("."))

        # compact: remove empty tokens, squash consecutive dots, cap length
        cand = TOKEN_SEP.join(t for t in tokens if t)
        cand = re.sub(r"\.{2,}", ".", cand).strip(".")
        return cand[:USERNAME_MAX_LEN]

    def next_unique(self, session, seed: UsernameSeed, exists_query) -> str:
        """
        Generate the first username that's not present in DB.
        `exists_query(session, username:str) -> bool` must return True if username exists.
        """
        # Try several pure-text variants before getting weirder
        for attempt in range(32):
            cand = self.propose(seed, attempt=attempt)
            if cand and not exists_query(session, cand):
                return cand
        # As a last resort, add an extra adjective token (still no numbers)
        for attempt in range(32, 64):
            cand = self.propose(seed, attempt=attempt) + f".{random.choice(self.adj)}"
            cand = re.sub(r"\.{2,}", ".", cand).strip(".")[:USERNAME_MAX_LEN]
            if not exists_query(session, cand):
                return cand
        raise RuntimeError("Could not generate a unique username without digits")
