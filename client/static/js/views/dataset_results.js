PANDA.views.DatasetResults = Backbone.View.extend({
    dataset: null,

    initialize: function(options) {
        _.bindAll(this);

        this.search = options.search;
    },

    set_dataset: function(dataset) {
        this.dataset = dataset;
        this.dataset.data.bind("reset", this.render);
    },

    render: function() {
        // Don't render search results if there was no search
        if (!this.search.query) {
            return;
        }

        var context = PANDA.utils.make_context(this.dataset.data.meta);

        context["query"] = this.search.query,
        context["root_url"] = "#dataset/" + this.dataset.get("slug") + "/search/" + this.search.encode_query_string();
        context["pager_unit"] = "row";
        context["row_count"] = this.dataset.get("row_count");
        context["dataset"] = this.dataset.results();

        context["pager"] = PANDA.templates.inline_pager(context);

        this.el.html(PANDA.templates.dataset_results(context));
    }
});
