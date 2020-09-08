from genelib.nested.data.universe import Universe


class ConsolationUniverse(Universe):
    class ItemGenerator(Universe.ItemGenerator):
        default_name = 'consolation universe'
