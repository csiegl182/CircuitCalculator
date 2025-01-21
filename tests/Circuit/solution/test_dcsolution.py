from pytest import MonkeyPatch
from CircuitCalculator.Circuit.solution import ComplexSolution
from CircuitCalculator.Circuit.circuit import Circuit

correct_voltage = 1+1j
other_voltage = 2+2j
correct_current = 3+3j
other_current = 4+4j
correct_potential = 5+5j
other_potential = 6+6j
correct_power = 1/2*correct_voltage*correct_current.conjugate()
other_power = 1/2*other_voltage*other_current.conjugate()

class NetworkSolutionMock:
    def get_voltage(self, branch_id: str) -> complex:
        if branch_id == 'correct_id':
            return correct_voltage
        return other_voltage
    def get_current(self, branch_id: str) -> complex:
        if branch_id == 'correct_id':
            return correct_current
        return other_current
    def get_potential(self, node_id: str) -> complex:
        if node_id == 'correct_id':
            return correct_potential
        return other_potential
    def get_power(self, branch_id: str) -> complex:
        if branch_id == 'correct_id':
            return correct_power
        return other_power

def test_complex_solution_returns_voltage_when_asking_for_correct_id(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('CircuitCalculator.Circuit.solution.transform', lambda _, w, rms: [None])

    complex_solution = ComplexSolution(Circuit([]), lambda _: NetworkSolutionMock(), peak_values=True)

    assert complex_solution.get_voltage('correct_id') == correct_voltage

def test_complex_solution_returns_voltage_when_asking_for_another_id(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('CircuitCalculator.Circuit.solution.transform', lambda _, w, rms: [None])

    complex_solution = ComplexSolution(Circuit([]), lambda _: NetworkSolutionMock(), peak_values=True)

    assert complex_solution.get_voltage('another_id') == other_voltage

def test_complex_solution_returns_current_when_asking_for_correct_id(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('CircuitCalculator.Circuit.solution.transform', lambda _, w, rms: [None])

    complex_solution = ComplexSolution(Circuit([]), lambda _: NetworkSolutionMock(), peak_values=True)

    assert complex_solution.get_current('correct_id') == correct_current

def test_complex_solution_returns_current_when_asking_for_another_id(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('CircuitCalculator.Circuit.solution.transform', lambda _, w, rms: [None])

    complex_solution = ComplexSolution(Circuit([]), lambda _: NetworkSolutionMock(), peak_values=True)

    assert complex_solution.get_current('another_id') == other_current

def test_complex_solution_returns_potential_when_asking_for_correct_id(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('CircuitCalculator.Circuit.solution.transform', lambda _, w, rms: [None])

    complex_solution = ComplexSolution(Circuit([]), lambda _: NetworkSolutionMock(), peak_values=True)

    assert complex_solution.get_potential('correct_id') == correct_potential

def test_complex_solution_returns_potential_when_asking_for_another_id(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('CircuitCalculator.Circuit.solution.transform', lambda _, w, rms: [None])

    complex_solution = ComplexSolution(Circuit([]), lambda _: NetworkSolutionMock(), peak_values=True)

    assert complex_solution.get_potential('another_id') == other_potential

def test_complex_solution_returns_power_when_asking_for_correct_id(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('CircuitCalculator.Circuit.solution.transform', lambda _, w, rms: [None])

    complex_solution = ComplexSolution(Circuit([]), lambda _: NetworkSolutionMock(), peak_values=True)

    assert complex_solution.get_power('correct_id') == correct_power

def test_complex_solution_returns_power_when_asking_for_another_id(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr('CircuitCalculator.Circuit.solution.transform', lambda _, w, rms: [None])

    complex_solution = ComplexSolution(Circuit([]), lambda _: NetworkSolutionMock(), peak_values=True)

    assert complex_solution.get_power('another_id') == other_power