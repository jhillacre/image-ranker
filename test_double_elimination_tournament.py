import pytest

from double_elimination_tournament import DoubleEliminationTournament


class TestDoubleEliminationTournament:
    def simulate_tournament(self, participants, match_outcome):
        """
        Simulate the tournament by automatically determining the winner based on the match_outcome function.
        Handles the generator to interactively provide winners and collect final standings.
        """
        tournament = DoubleEliminationTournament(participants)
        gen = tournament.run_tournament()
        match_log = []

        try:
            (a, b) = next(gen)
            # byes should not be 'played', tournaments of one or zero will StopIteration immediately
            assert a is not None
            assert b is not None
            while True:
                winner = match_outcome(a, b)

                # Send the winner back to the generator
                (a, b) = gen.send(winner)

                # byes should not be 'played'
                assert a is not None
                assert b is not None
        except StopIteration as e:
            # Final standings are returned via StopIteration exception
            standings = e.value
            return list(standings) if standings else []

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (set(), []),
            ({"A"}, ["A"]),
            ({"A", "B"}, ["B", "A"]),
            (
                {
                    "A": True,
                    "B": True,
                    "C": True,
                    "D": True,
                    "E": True,
                    "F": True,
                    "G": True,
                },
                ["G", "F", "D", "E", "B", "C", "A"],
            ),
            (
                {
                    "A": True,
                    "B": True,
                    "C": True,
                    "D": True,
                    "E": True,
                    "F": True,
                    "G": True,
                    "H": True,
                },
                ["H", "G", "D", "F", "B", "C", "E", "A"],
            ),
        ],
    )
    def test_tournament_sizes(self, test_input, expected):
        def match_outcome(a, b):
            return a if a > b else b

        standings = self.simulate_tournament(test_input, match_outcome)
        assert standings == expected
