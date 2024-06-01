from typing import Any, Dict, Generator, List, Tuple, Union

immutable_type = Union[int, float, str, bool, tuple, frozenset, bytes]


class DoubleEliminationTournament:
    def __init__(self, participants: Union[set, Dict[immutable_type, Any]]):
        """
        Initializes the double elimination tournament with participants.
        """
        if isinstance(participants, set):
            participants = {participant: True for participant in participants}

        self.participants = participants
        self.winners_bracket = list(participants.keys())
        self.losers_bracket = []
        self.standings = []

    def run_tournament(
        self,
    ) -> Generator[
        Tuple[immutable_type, immutable_type], immutable_type, List[immutable_type]
    ]:
        """
        Generator to run the double elimination tournament. Yields pairs of participants to compete in a match and
        accepts the winner of each match.
        """
        # Run the tournament until there is only one winner in the winners bracket and one winner in the losers bracket.
        while len(self.winners_bracket) > 1 or len(self.losers_bracket) > 1:
            # Losers Bracket, if applicable. the losers bracket will continue more rounds than the winners bracket
            if len(self.losers_bracket) > 1:
                for a, b in self.prepare_matches(self.losers_bracket):
                    if b is None:
                        winner = a
                    else:
                        winner = yield (a, b)
                    self.process_match_result(
                        (a, b), winner, self.losers_bracket, self.standings
                    )

            # Winners Bracket, if applicable. the winners bracket will finish before the losers bracket
            if len(self.winners_bracket) > 1:
                for a, b in self.prepare_matches(self.winners_bracket):
                    if b is None:
                        winner = a
                    else:
                        winner = yield (a, b)
                    self.process_match_result(
                        (a, b), winner, self.winners_bracket, self.losers_bracket
                    )

        # Grand Final
        if len(self.winners_bracket) == 1 and len(self.losers_bracket) == 1:
            winners_champion = self.winners_bracket[0]
            losers_champion = self.losers_bracket[0]
            final_winner = yield (winners_champion, losers_champion)
            second_place = (
                losers_champion
                if final_winner == winners_champion
                else winners_champion
            )
            self.standings.append(second_place)
            self.standings.append(final_winner)
            return list(
                reversed(self.standings)
            )  # Final standings can also be yielded or returned.
        # this is an exception.
        # this means no grand final was run, and the tournament is over.
        return list(self.participants.keys())

    def prepare_matches(
        self, bracket: List[immutable_type]
    ) -> List[Tuple[immutable_type, immutable_type]]:
        """
        Prepare pairs of participants for matches from the given bracket.
        """
        # Adding a bye if the number of participants is odd.
        if len(bracket) % 2 != 0:
            bracket.append(None)
        return [(bracket[i], bracket[i + 1]) for i in range(0, len(bracket), 2)]

    def process_match_result(
        self,
        match: Tuple[immutable_type, immutable_type],
        winner: immutable_type,
        current_bracket: List[immutable_type],
        next_bracket: List[immutable_type],
    ):
        """
        Process the match result, updating brackets accordingly.
        """
        # if the winner is None, it is an usage error
        if not winner:
            raise ValueError("Winner must be provided via generator send.")
        loser = match[0] if winner == match[1] else match[1]
        current_bracket.remove(loser)
        # if it's not a bye, add loser to the next bracket
        if loser:
            next_bracket.append(loser)
