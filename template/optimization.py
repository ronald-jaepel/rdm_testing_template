import numpy as np
from CADETProcess import settings
# from CADETProcess.optimization import GPEI
from CADETProcess.optimization import OptimizationProblem
from CADETProcess.optimization import U_NSGA3
from cadetrdm import Options

STUDY_NAME = 'template'

DEFAULT_OPTIONS = Options({
    'temp_directory_base': None,
    'cache_directory_base': None,
})


def setup_optimization_problem(user_options):
    options = DEFAULT_OPTIONS.copy()
    if user_options is not None:
        options.update(user_options)

    name = f"{STUDY_NAME}"

    if options.temp_directory_base is not None:
        settings.temp_dir = options.temp_directory_base / name / options.get_hash()
        print(settings.temp_dir)

    if options.cache_directory_base is None:
        cache_directory = None
    else:
        cache_directory = options.cache_directory_base / name / options.get_hash()
        print(cache_directory)

    optimization_problem = OptimizationProblem(
        name="problem",
        cache_directory=cache_directory
    )

    # gradient1 start concentration
    optimization_problem.add_variable("x0", lb=-5, ub=5)
    optimization_problem.add_variable("x1", lb=-5, ub=5)

    optimization_problem.add_nonlinear_constraint(
        lambda x: x[0] + x[1],
        bounds=5,
        evaluation_objects=None,
        name="nonlinear_constraint"
    )

    optimization_problem.add_objective(
        lambda x: (x[0] - 1) ** 2 + (x[1] + 1) ** 2 + np.sin(x[0] * 10) * 2 + np.sin(x[1] * 5)
    )

    return optimization_problem


def setup_optimizer(optimization_problem, optimizer_options):
    if optimizer_options['optimizer'] == 'U_NSGA3':
        optimizer = U_NSGA3()
        default_options = {
            "n_cores": -4,
            "pop_size": optimization_problem.n_variables * 16,
            "n_max_gen": 5,
        }
    else:
        raise ValueError(f"Unknown optimizer: {optimizer_options.optimizer}")

    default_options.update(optimizer_options)
    for key, value in default_options.items():
        setattr(optimizer, key, value)

    return optimizer


def run_optimizer():
    optimization_problem = setup_optimization_problem(None)

    optimizer = setup_optimizer(
        optimization_problem,
        Options(
            {
                "optimizer": "U_NSGA3",
            }),
    )

    results = optimizer.optimize(
        optimization_problem,
        save_results=True,
        use_checkpoint=False,
        results_directory=f"tmp",
    )


if __name__ == '__main__':
    run_optimizer()
