"""Discipline registry and reference definitions."""

from __future__ import annotations

import math

from ENGINEERING.engineering_models import DisciplineSpecification, DisciplineType


def _ratio(numerator: float, denominator: float) -> float:
    if denominator == 0.0:
        raise ValueError("denominator must not be zero")
    return numerator / denominator


class EngineeringRegistry:
    """Registry of discipline specifications, rules, and default calculations."""

    def __init__(self) -> None:
        self._specs = self._build_specs()

    def get(self, discipline: DisciplineType) -> DisciplineSpecification:
        """Return a discipline specification."""
        return self._specs[discipline]

    def discipline_names(self) -> list[str]:
        """Return all discipline names."""
        return [discipline.value for discipline in self._specs]

    def default_calculation_name(self, discipline: DisciplineType) -> str:
        """Return the default calculation name for a discipline."""
        return self.get(discipline).default_calculation_name

    def sample_inputs(self, discipline: DisciplineType) -> dict[str, float]:
        """Return sample inputs for the discipline default calculation."""
        spec = self.get(discipline)
        return dict(spec.sample_inputs[spec.default_calculation_name])

    @staticmethod
    def _build_specs() -> dict[DisciplineType, DisciplineSpecification]:
        return {
            DisciplineType.MECHANICAL_ENGINEERING: DisciplineSpecification(
                discipline=DisciplineType.MECHANICAL_ENGINEERING,
                default_calculation_name="beam_bending_stress",
                calculation_units={"beam_bending_stress": "MPa"},
                formulas={"beam_bending_stress": lambda data: data["moment_nm"] * 1000.0 / data["section_modulus_mm3"]},
                required_inputs={"beam_bending_stress": ("moment_nm", "section_modulus_mm3")},
                sample_inputs={"beam_bending_stress": {"moment_nm": 1200.0, "section_modulus_mm3": 60000.0}},
                design_rules=["Maintain safety factor above 1.5 for general machinery."],
                standards=["ASME Y14.5", "ISO 2768"],
                library={"common_components": ["shaft", "bearing", "bracket"]},
                future_interfaces=["multibody_solver", "fatigue_solver"],
            ),
            DisciplineType.CIVIL_ENGINEERING: DisciplineSpecification(
                discipline=DisciplineType.CIVIL_ENGINEERING,
                default_calculation_name="slab_load",
                calculation_units={"slab_load": "kN"},
                formulas={"slab_load": lambda data: data["area_m2"] * data["pressure_kpa"]},
                required_inputs={"slab_load": ("area_m2", "pressure_kpa")},
                sample_inputs={"slab_load": {"area_m2": 30.0, "pressure_kpa": 6.0}},
                design_rules=["Respect serviceability deflection limits and load combinations."],
                standards=["ACI 318", "Eurocode 2"],
                library={"site_assets": ["slab", "beam", "retaining_wall"]},
                future_interfaces=["soil_solver", "hydrology_solver"],
            ),
            DisciplineType.STRUCTURAL_ENGINEERING: DisciplineSpecification(
                discipline=DisciplineType.STRUCTURAL_ENGINEERING,
                default_calculation_name="column_capacity",
                calculation_units={"column_capacity": "kN"},
                formulas={"column_capacity": lambda data: data["area_mm2"] * data["yield_strength_mpa"] / 1000.0},
                required_inputs={"column_capacity": ("area_mm2", "yield_strength_mpa")},
                sample_inputs={"column_capacity": {"area_mm2": 3500.0, "yield_strength_mpa": 250.0}},
                design_rules=["Target structural safety factors above 1.67 for primary load paths."],
                standards=["AISC 360", "Eurocode 3"],
                library={"members": ["column", "truss", "brace"]},
                future_interfaces=["buckling_solver", "seismic_solver"],
            ),
            DisciplineType.ARCHITECTURE: DisciplineSpecification(
                discipline=DisciplineType.ARCHITECTURE,
                default_calculation_name="space_efficiency",
                calculation_units={"space_efficiency": "%"},
                formulas={"space_efficiency": lambda data: _ratio(data["usable_area_m2"], data["gross_area_m2"]) * 100.0},
                required_inputs={"space_efficiency": ("usable_area_m2", "gross_area_m2")},
                sample_inputs={"space_efficiency": {"usable_area_m2": 420.0, "gross_area_m2": 500.0}},
                design_rules=["Promote circulation efficiency and code-compliant egress."],
                standards=["IBC", "ADA"],
                library={"spaces": ["core", "circulation", "enclosure"]},
                future_interfaces=["occupancy_solver", "daylight_solver"],
            ),
            DisciplineType.ELECTRICAL_ENGINEERING: DisciplineSpecification(
                discipline=DisciplineType.ELECTRICAL_ENGINEERING,
                default_calculation_name="ohms_law_current",
                calculation_units={"ohms_law_current": "A"},
                formulas={"ohms_law_current": lambda data: _ratio(data["voltage_v"], data["resistance_ohm"])},
                required_inputs={"ohms_law_current": ("voltage_v", "resistance_ohm")},
                sample_inputs={"ohms_law_current": {"voltage_v": 24.0, "resistance_ohm": 8.0}},
                design_rules=["Respect circuit protection and voltage-drop limits."],
                standards=["NEC", "IEC 60364"],
                library={"elements": ["bus", "connector", "fuse"]},
                future_interfaces=["signal_integrity_solver", "power_flow_solver"],
            ),
            DisciplineType.PLUMBING: DisciplineSpecification(
                discipline=DisciplineType.PLUMBING,
                default_calculation_name="pipe_flow_rate",
                calculation_units={"pipe_flow_rate": "L/s"},
                formulas={"pipe_flow_rate": lambda data: data["velocity_m_s"] * data["area_m2"] * 1000.0},
                required_inputs={"pipe_flow_rate": ("velocity_m_s", "area_m2")},
                sample_inputs={"pipe_flow_rate": {"velocity_m_s": 1.6, "area_m2": 0.003}},
                design_rules=["Keep sanitary and supply systems serviceable and code-compliant."],
                standards=["IPC", "UPC"],
                library={"systems": ["supply", "waste", "vent"]},
                future_interfaces=["pressure_loss_solver", "network_solver"],
            ),
            DisciplineType.HVAC: DisciplineSpecification(
                discipline=DisciplineType.HVAC,
                default_calculation_name="air_change_rate",
                calculation_units={"air_change_rate": "ACH"},
                formulas={"air_change_rate": lambda data: data["airflow_m3_s"] * 3600.0 / data["room_volume_m3"]},
                required_inputs={"air_change_rate": ("airflow_m3_s", "room_volume_m3")},
                sample_inputs={"air_change_rate": {"airflow_m3_s": 2.5, "room_volume_m3": 300.0}},
                design_rules=["Maintain air exchange and thermal comfort targets."],
                standards=["ASHRAE 62.1", "ASHRAE 55"],
                library={"equipment": ["air_handler", "duct", "diffuser"]},
                future_interfaces=["psychrometric_solver", "energy_model"],
            ),
            DisciplineType.MANUFACTURING: DisciplineSpecification(
                discipline=DisciplineType.MANUFACTURING,
                default_calculation_name="process_efficiency",
                calculation_units={"process_efficiency": "%"},
                formulas={"process_efficiency": lambda data: _ratio(data["ideal_cycle_time_s"], data["actual_cycle_time_s"]) * 100.0},
                required_inputs={"process_efficiency": ("ideal_cycle_time_s", "actual_cycle_time_s")},
                sample_inputs={"process_efficiency": {"ideal_cycle_time_s": 42.0, "actual_cycle_time_s": 50.0}},
                design_rules=["Prefer manufacturable geometry and realistic tolerance stacks."],
                standards=["ISO 9001", "ASME B46.1"],
                library={"processes": ["milling", "turning", "additive"]},
                future_interfaces=["cam_solver", "factory_optimizer"],
            ),
            DisciplineType.MATERIALS_ENGINEERING: DisciplineSpecification(
                discipline=DisciplineType.MATERIALS_ENGINEERING,
                default_calculation_name="specific_strength",
                calculation_units={"specific_strength": "MPa/(g/cm^3)"},
                formulas={"specific_strength": lambda data: _ratio(data["strength_mpa"], data["density_g_cm3"])},
                required_inputs={"specific_strength": ("strength_mpa", "density_g_cm3")},
                sample_inputs={"specific_strength": {"strength_mpa": 550.0, "density_g_cm3": 2.7}},
                design_rules=["Balance strength, density, corrosion, and process compatibility."],
                standards=["ASTM E8", "ISO 6892"],
                library={"families": ["metals", "polymers", "composites"]},
                future_interfaces=["creep_solver", "microstructure_model"],
            ),
            DisciplineType.ROBOTICS: DisciplineSpecification(
                discipline=DisciplineType.ROBOTICS,
                default_calculation_name="reach_index",
                calculation_units={"reach_index": "m/kg"},
                formulas={"reach_index": lambda data: _ratio(data["reach_m"], data["payload_kg"])},
                required_inputs={"reach_index": ("reach_m", "payload_kg")},
                sample_inputs={"reach_index": {"reach_m": 1.8, "payload_kg": 12.0}},
                design_rules=["Preserve workspace reach without overloading the manipulator."],
                standards=["ISO 10218", "RIA R15.06"],
                library={"subsystems": ["arm", "end_effector", "sensor"]},
                future_interfaces=["path_planner", "control_tuner"],
            ),
            DisciplineType.AUTOMOTIVE_ENGINEERING: DisciplineSpecification(
                discipline=DisciplineType.AUTOMOTIVE_ENGINEERING,
                default_calculation_name="power_to_weight",
                calculation_units={"power_to_weight": "kW/tonne"},
                formulas={"power_to_weight": lambda data: _ratio(data["power_kw"], data["mass_kg"] / 1000.0)},
                required_inputs={"power_to_weight": ("power_kw", "mass_kg")},
                sample_inputs={"power_to_weight": {"power_kw": 220.0, "mass_kg": 1320.0}},
                design_rules=["Balance mass, drag, thermal load, and serviceability."],
                standards=["SAE J1100", "FMVSS"],
                library={"systems": ["chassis", "powertrain", "aero"]},
                future_interfaces=["vehicle_dynamics_solver", "cooling_model"],
            ),
            DisciplineType.AEROSPACE_ENGINEERING: DisciplineSpecification(
                discipline=DisciplineType.AEROSPACE_ENGINEERING,
                default_calculation_name="thrust_to_weight",
                calculation_units={"thrust_to_weight": "ratio"},
                formulas={"thrust_to_weight": lambda data: _ratio(data["thrust_n"], data["mass_kg"] * 9.81)},
                required_inputs={"thrust_to_weight": ("thrust_n", "mass_kg")},
                sample_inputs={"thrust_to_weight": {"thrust_n": 180000.0, "mass_kg": 15000.0}},
                design_rules=["Track mass fraction, thermal load, and structural margins."],
                standards=["NASA-STD-5001", "ECSS"],
                library={"systems": ["fuselage", "propulsion", "guidance"]},
                future_interfaces=["trajectory_solver", "aeroelastic_model"],
            ),
            DisciplineType.THERMODYNAMICS: DisciplineSpecification(
                discipline=DisciplineType.THERMODYNAMICS,
                default_calculation_name="heat_energy",
                calculation_units={"heat_energy": "kJ"},
                formulas={"heat_energy": lambda data: data["mass_kg"] * data["specific_heat_kj_kgk"] * data["delta_t_k"]},
                required_inputs={"heat_energy": ("mass_kg", "specific_heat_kj_kgk", "delta_t_k")},
                sample_inputs={"heat_energy": {"mass_kg": 5.0, "specific_heat_kj_kgk": 4.2, "delta_t_k": 20.0}},
                design_rules=["Respect first-law consistency and thermal boundary assumptions."],
                standards=["ASHRAE Fundamentals", "ISO 80000"],
                library={"concepts": ["enthalpy", "entropy", "heat_exchanger"]},
                future_interfaces=["cycle_solver", "transient_thermal_model"],
            ),
            DisciplineType.COMBUSTION_ENGINEERING: DisciplineSpecification(
                discipline=DisciplineType.COMBUSTION_ENGINEERING,
                default_calculation_name="energy_release_index",
                calculation_units={"energy_release_index": "MJ/kg"},
                formulas={"energy_release_index": lambda data: _ratio(data["fuel_energy_mj"], data["fuel_mass_kg"])},
                required_inputs={"energy_release_index": ("fuel_energy_mj", "fuel_mass_kg")},
                sample_inputs={"energy_release_index": {"fuel_energy_mj": 86.0, "fuel_mass_kg": 2.0}},
                design_rules=["Maintain safe mixture assumptions and thermal containment."],
                standards=["NFPA 85", "API 560"],
                library={"systems": ["burner", "chamber", "exhaust"]},
                future_interfaces=["reaction_solver", "emissions_model"],
            ),
            DisciplineType.FLUID_MECHANICS: DisciplineSpecification(
                discipline=DisciplineType.FLUID_MECHANICS,
                default_calculation_name="reynolds_number",
                calculation_units={"reynolds_number": "dimensionless"},
                formulas={"reynolds_number": lambda data: data["density_kg_m3"] * data["velocity_m_s"] * data["diameter_m"] / data["viscosity_pa_s"]},
                required_inputs={"reynolds_number": ("density_kg_m3", "velocity_m_s", "diameter_m", "viscosity_pa_s")},
                sample_inputs={"reynolds_number": {"density_kg_m3": 998.0, "velocity_m_s": 2.0, "diameter_m": 0.05, "viscosity_pa_s": 0.001}},
                design_rules=["Track regime transitions and pressure-loss implications."],
                standards=["Crane TP-410", "ASHRAE Handbook"],
                library={"components": ["pipe", "nozzle", "plenum"]},
                future_interfaces=["network_flow_solver", "turbulence_model"],
            ),
            DisciplineType.ASTRONOMY: DisciplineSpecification(
                discipline=DisciplineType.ASTRONOMY,
                default_calculation_name="angular_resolution",
                calculation_units={"angular_resolution": "rad"},
                formulas={"angular_resolution": lambda data: 1.22 * data["wavelength_m"] / data["aperture_m"]},
                required_inputs={"angular_resolution": ("wavelength_m", "aperture_m")},
                sample_inputs={"angular_resolution": {"wavelength_m": 5.5e-7, "aperture_m": 2.4}},
                design_rules=["Preserve optical throughput and pointing stability assumptions."],
                standards=["IAU conventions", "NASA optical standards"],
                library={"instruments": ["telescope", "detector", "mount"]},
                future_interfaces=["observation_planner", "pointing_model"],
            ),
            DisciplineType.ORBITAL_MECHANICS: DisciplineSpecification(
                discipline=DisciplineType.ORBITAL_MECHANICS,
                default_calculation_name="orbital_velocity",
                calculation_units={"orbital_velocity": "km/s"},
                formulas={"orbital_velocity": lambda data: math.sqrt(data["gravitational_parameter"] / data["radius_km"])},
                required_inputs={"orbital_velocity": ("gravitational_parameter", "radius_km")},
                sample_inputs={"orbital_velocity": {"gravitational_parameter": 398600.4418, "radius_km": 7000.0}},
                design_rules=["Preserve orbital energy consistency and reference-frame clarity."],
                standards=["NASA SP-8021", "CCSDS"],
                library={"elements": ["orbit", "transfer", "attitude"]},
                future_interfaces=["n_body_solver", "maneuver_optimizer"],
            ),
            DisciplineType.SCIENTIFIC_CALCULATIONS: DisciplineSpecification(
                discipline=DisciplineType.SCIENTIFIC_CALCULATIONS,
                default_calculation_name="root_mean_square",
                calculation_units={"root_mean_square": "units"},
                formulas={"root_mean_square": lambda data: math.sqrt(sum(value * value for value in (data["x1"], data["x2"], data["x3"])) / 3.0)},
                required_inputs={"root_mean_square": ("x1", "x2", "x3")},
                sample_inputs={"root_mean_square": {"x1": 3.0, "x2": 4.0, "x3": 5.0}},
                design_rules=["Use dimensionally consistent scientific inputs and outputs."],
                standards=["ISO 80000", "NIST SP 811"],
                library={"methods": ["interpolation", "integration", "statistics"]},
                future_interfaces=["symbolic_solver", "scientific_notebook"],
            ),
        }