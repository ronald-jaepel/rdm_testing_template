from cadetrdm import Options
from cadetrdm.wrapper import tracks_results

from template import setup_optimization_problem, setup_optimizer


@tracks_results
def main(repo, options):
    optimization_problem = setup_optimization_problem(options)

    pop_size_per_independent_variable = options.optimizer_options.pop(
        "pop_size_per_independent_variable", None
    )
    if pop_size_per_independent_variable is not None:
        assert "pop_size" not in options.optimier_options, (
            "'pop_size' and 'pop_size_per_independent_variable' were specified. "
            "Decide for one option."
        )

        pop_size = (
            optimization_problem.n_independent_variables *
            pop_size_per_independent_variable
        )
        options.optimizer_options["pop_size"] = pop_size

    optimizer = setup_optimizer(optimization_problem, options.optimizer_options)
    results = optimizer.optimize(
        optimization_problem,
        save_results=True,
        use_checkpoint=False,
        results_directory=f"{repo.output_path}",
    )


if __name__ == '__main__':
    options = Options()
    options.debug = True
    options.push = False
    options.commit_message = 'Trying out new things'
    options.optimizer_options = {
        "optimizer": "U_NSGA3",
        "pop_size": 20,
        "n_cores": 10,
        "n_max_gen": 3,
    }
    main(options)
