if (typeof gettext != "function") {
    gettext = function(identifier) {
        return identifier;
    }
}

Music = {
    pageNum: 1,
    hasNextPage: true,
    options: {},
    searchOptions: {},
    infiniteScrollActive: false,
    sessionPing: 60000,
    csrf_token: null,

    init: function() {
        Music.csrf_token = $('#csrf_token input').val();

        $(".loadList").bind("click", function() {
            Music.options = {};
            Music.setActiveMenu($(this));
            Music.loadList($(this).attr("href"));
            return false;
        });

        $("#searchform span.searchsubmit").bind("click", function() {
            Music.options = {"search_term": $("input.searchterm").val()};
            Music.loadList("/api/v1/songs");
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            return false;
        });
        $("#searchform").bind("submit", function() {
            Music.options = {"search_term": $("input.searchterm").val()};
            Music.loadList("/api/v1/songs");
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            return false;
        });

        $("#searchdetailsform span.searchsubmit").bind("click", function() {
            Music.options = Music.getSearchOptions();
            Music.loadList("/api/v1/songs");
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            $("#searchoptions").click();
            return false;
        });
        $("#searchdetailsform span.searchreset").bind("click", function() {
            $("#search_title").val("");
            $("#search_artist").val("");
            $("#search_album").val("");
            $("#search_genre").val("");
            $("#search_year").val("");
            return false;
        });
        $("#searchdetailsform").bind("submit", function() {
            Music.options = Music.getSearchOptions();
            Music.loadList("/api/v1/songs");
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            $("#searchoptions").click();
            return false;
        });
        // chrome doesn't fire submit on #searchdetailsform -> dirty workaround
        $("#search_title, #search_artist, #search_album, #search_album").bind("keydown", function() {
            if (event.which == 13) {
                Music.options = Music.getSearchOptions();
                Music.loadList("/api/v1/songs");
                Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
                $("#searchoptions").click();
                return false;
            }
        });

        $("#searchoptions").bind("click", function() {
            if ($("#searchdetails:visible").length == 1) {
                $(document).unbind("click.search");
                $("#searchdetails").hide();
            }
            else {
                // reset all
                $("#searchdetailsform span.searchreset").click();

                // fill form by current search options
                $.each(Music.searchOptions, function(key, value) {
                    if (key != "genre_id" && value.substr(0, 1) == "(") {
                        value = value.substr(1, value.length - 2);
                    }
                    switch (key) {
                        case "title":
                            $("#search_title").val(value);
                            break;
                        case "artist":
                            $("#search_artist").val(value);
                            break;
                        case "album":
                            $("#search_album").val(value);
                            break;
                        case "genre_id":
                            $("#search_genre").val(value);
                            break;
                        case "year":
                            $("#search_year").val(value);
                            break;
                    }
                });

                $("#searchdetails").show();
                $(document).bind("click.search", function(event) {
                    if ($(event.target).closest("#searchdetails").length == 0 && $(event.target).closest("#searchoptions").length == 0) {
                        $("#searchoptions").click();
                    }
                });
            }
        });

        $("#profile").bind("click", function() {
            if ($("#accountoptions:visible").length == 1) {
                $(document).unbind("click.account");
                $("#accountoptions").hide();
            }
            else {
                $("#accountoptions").show();
                $(document).bind("click.account", function(event) {
                    if ($(event.target).closest("#accountoptions").length == 0 && $(event.target).closest("#profile").length == 0) {
                        $("#profile").click();
                    }
                });
            }
        });

        $("#main table.list td.filter").live("click", function() {
            var value = $(this).attr("data-value");
            if ($(this).hasClass("filter_artist")) {
                Music.options = {"filter_artist_id": value};
            }
            else if ($(this).hasClass("filter_album")) {
                Music.options = {"filter_album_id": value};
            }
            else if ($(this).hasClass("filter_genre")) {
                Music.options = {"filter_genre": value};
            }
            else if ($(this).hasClass("filter_year")) {
                Music.options = {"filter_year": value};
            }
            else if ($(this).hasClass("search_title")) {
                Music.options = {"search_title": value};
            }
            Music.loadList("/api/v1/songs");
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            return false;
        });

        $("#main table.list th").live("click", function() {
            if ($(this).hasClass("sort_asc")) {
                Music.options.order_direction = "desc";
            }
            else {
                Music.options.order_direction = "asc";
            }

            if ($(this).hasClass("sort_title")) {
                Music.options.order_by = "title";
            }
            else if ($(this).hasClass("sort_artist")) {
                Music.options.order_by = "artist";
            }
            else if ($(this).hasClass("sort_album")) {
                Music.options.order_by = "album";
            }
            else if ($(this).hasClass("sort_genre")) {
                Music.options.order_by = "genre";
            }
            else if ($(this).hasClass("sort_year")) {
                Music.options.order_by = "year";
            }
            else if ($(this).hasClass("sort_length")) {
                Music.options.order_by = "length";
            }
            else if ($(this).hasClass("sort_created")) {
                Music.options.order_by = "created";
            }
            else if ($(this).hasClass("sort_votes")) {
                Music.options.order_by = "votes";
            }

            switch ($(this).closest("tr").attr("class")) {
                case "queue":
                    Music.loadList("/api/v1/queue");
                    break;
                case "history":
                    Music.loadList("/api/v1/history");
                    break;
                case "history_my":
                    Music.loadList("/api/v1/history/my");
                    break;
                case "favourites":
                    Music.loadList("/api/v1/favourites");
                    break;
                case "songs":
                    Music.loadList("/api/v1/songs");
                    break;
                case "artists":
                    Music.loadList("/api/v1/artists");
                    break;
                case "albums":
                    Music.loadList("/api/v1/albums");
                    break;
                case "genres":
                    Music.loadList("/api/v1/genres");
                    break;
                case "years":
                    Music.loadList("/api/v1/years");
                    break;
            }

            return false;
        });

        $("#main table.list img.queue_add").live("click", function() {
            $.ajax({
                url: "/api/v1/queue",
                type: "POST",
                data: {
                    "id": $(this).attr("data-id"),
                    "csrfmiddlewaretoken": Music.csrf_token
                },
                success: function(data) {
                    var item = $("img.queue_add[data-id=" + data.id + "]");
                    item.attr("src", "/static/img/queue_active.png");
                    item.removeClass("queue_add");
                    item.addClass("queue_remove");
                    item.attr("id", item.attr("id").replace(/add/, "remove"));
                    item.attr("alt", gettext("Revoke vote"));
                    item.attr("title", gettext("Revoke vote"));
                    item.closest("tr").find(".voteCount").html(data.count);
                }
            });
            return false;
        });

        $("#main table.list img.queue_remove").live("click", function() {
            var success = null;
            if ($(this).closest("tr.row_queue").length == 0) {
                success = function(data) {
                    var item = $("img.queue_remove[data-id=" + data.id + "]");
                    item.attr("src", "/static/img/queue.png");
                    item.removeClass("queue_remove");
                    item.addClass("queue_add");
                    item.attr("id", item.attr("id").replace(/remove/, "add"));
                    item.attr("alt", gettext("Vote to play"));
                    item.attr("title", gettext("Vote to play"));
                };
            }
            else {
                success = function(data) {
                    var item = $("img.queue_remove[data-id=" + data.id + "]");

                    if (data.count == 0) {
                        item.closest("tr").fadeOut(1000, function() {
                            item.closest("tr").remove();
                        });
                        return;
                    }
                    item.attr("src", "/static/img/queue.png");
                    item.removeClass("queue_remove");
                    item.addClass("queue_add");
                    item.attr("id", item.attr("id").replace(/remove/, "add"));
                    item.attr("alt", gettext("Support vote"));
                    item.attr("title", gettext("Support vote"));
                    item.closest("tr").find(".voteCount").html(data.count);
                };
            }

            $.ajax({
                url: "/api/v1/queue/" + $(this).attr("data-id"),
                type: "DELETE",
                success: function(data) {
                    success(data);
                }
            });
            return false;
        });

        $("#main table.list img.favourite_add").live("click", function() {
            $.ajax({
                url: "/api/v1/favourites",
                type: "POST",
                data: {
                    "id": $(this).attr("data-id"),
                    "csrfmiddlewaretoken": Music.csrf_token
                },
                success: function(data) {
                    var item = $("img.favourite_add[data-id=" + data.id + "]");
                    item.attr("src", "/static/img/favourite_active.png");
                    item.removeClass("favourite_add");
                    item.addClass("favourite_remove");
                    item.attr("id", item.attr("id").replace(/add/, "remove"));
                    item.attr("alt", gettext("Remove from favourites"));
                    item.attr("title", gettext("Remove from favourites"));
                }
            });
            return false;
        });

        $("#main table.list img.favourite_remove").live("click", function() {
            var success = null;
            if ($(this).closest("tr.row_favourites").length == 0) {
                success = function(data) {
                    var item = $("img.favourite_remove[data-id=" + data.id + "]");
                    item.attr("src", "/static/img/favourite.png");
                    item.removeClass("favourite_remove");
                    item.addClass("favourite_add");
                    item.attr("id", item.attr("id").replace(/remove/, "add"));
                    item.attr("alt", gettext("Add to favourites"));
                    item.attr("title", gettext("Add to favourites"));
                };
            }
            else {
                success = function(data) {
                    var item = $("img.favourite_remove[data-id=" + data.id + "]");
                    item.closest("tr").fadeOut(1000, function() {
                        item.closest("tr").remove();
                    });
                };
            }

            $.ajax({
                url: "/api/v1/favourites/" + $(this).attr("data-id"),
                type: "DELETE",
                success: function(data) {
                    success(data);
                }
            });
            return false;
        });

        $("td.voteCount").live({
            mouseenter: function() {
                var element = $(this);
                var tooltip = $(this).find('div.voteTooltip');
                if (tooltip.length == 1) {
                    tooltip.css('left', element.offset().left - $(window).scrollLeft() + 50);
                    tooltip.css('top', element.offset().top - $(window).scrollTop() + 10);
                    tooltip.show();
                }
            },
            mouseleave: function() {
                var tooltip = $(this).find('div.voteTooltip');
                if (tooltip.length == 1) {
                    tooltip.hide();
                }
            }
        });

        $.ajaxSetup({
            type: "GET",
            cache: false,
            dataType: "json"
        });

        setTimeout("Music.ping()", Music.sessionPing);

        Music.loadList("/api/v1/queue");
        Music.setActiveMenu($("#sidebar ul li a.loadQueue"));
    },

    ping: function() {
        $.ajax({
            url: "/api/v1/ping",
            success: function() {
                setTimeout("Music.ping()", Music.sessionPing);
            }
        });
    },

    getSearchOptions: function() {
        var options = {};

        var value = $("#search_title").val();
        if (value.length > 0) {
            options.search_title = value;
        }
        var value = $("#search_artist").val();
        if (value.length > 0) {
            options.search_artist = value;
        }
        var value = $("#search_album").val();
        if (value.length > 0) {
            options.search_album = value;
        }
        var item = $("#search_genre").find("option:selected");
        if (item.length > 0 && item.val().length > 0) {
            options.filter_genre = item.val();
        }
        var item = $("#search_year").find("option:selected");
        if (item.length > 0 && item.val().length > 0) {
            options.filter_year = item.val();
        }

        return options;
    },

    setActiveMenu: function(item) {
        $("#sidebar").find("li").removeClass("active");
        item.closest("li").addClass("active");
    },

    loadList: function(url) {
        Music.pageNum = 1;
        Music.hasNextPage = false;
        Music.searchOptions = {};
        $("#searchdetailsform span.searchreset").click();

        // build options
        Music.options.page = Music.pageNum;
        Music.options.count = 30;

        $.ajax({
            url: url,
            data: Music.options,
            success: function(data) {
                $(window).unbind("scroll");
                $(window).scrollTop(0);

                Music.hasNextPage = data.hasNextPage;
                if (data.itemList.length > 0) {
                    $("#main").html(Music.renderTable(data));
                    $("#main table.list tbody").append(Music.renderData(data));
                }
                else {
                    $("#main").html("<div class=\"noContent\">" + gettext("No data found") + "</div>");
                }

                // set search term - don't iterate to get correct order
                Music.searchOptions = data.search;
                terms = [];
                if (data.search.title) {
                    terms.push("title:" + data.search.title);
                }
                if (data.search.artist) {
                    terms.push("artist:" + data.search.artist);
                }
                if (data.search.album) {
                    terms.push("album:" + data.search.album);
                }
                if (data.search.genre) {
                    terms.push("genre:" + data.search.genre);
                }
                if (data.search.year) {
                    terms.push("year:" + data.search.year);
                }
                if (data.search.term) {
                    terms.push(data.search.term);
                }
                $("input.searchterm").val(terms.join(" "));

                // load data until page is populated
                if (Music.hasNextPage && Music.getScrollHeight() <= $(document).height()) {
                    $(window).unbind("scroll");
                    Music.loadItems(url, Music.options);
                }
            }
        });
    },

    loadOnScroll: function(event) {
        if (Music.infiniteScrollActive === true) {
            return false;
        }

        if (Music.hasNextPage && Music.getScrollHeight() > Music.getDocumentHeight()) {
            $(window).unbind("scroll");
            Music.loadItems(event.data.url, event.data.options);
        }
    },

    getScrollHeight: function() {
        return $(window).scrollTop() + $(window).height();
    },

    getDocumentHeight: function() {
        return $(document).height() - $(document).height() * 0.2;
    },

    loadItems: function(url, options) {
        if (Music.hasNextPage === false) {
            return false;
        }

        if (typeof options == "undefined") {
            options = {};
        }

        Music.infiniteScrollActive = true;
        Music.pageNum = Music.pageNum + 1;

        options.page = Music.pageNum;
        options.count = 30;

        $.ajax({
            url: url.replace(/\[page\]/, Music.pageNum),
            data: options,
            success: function(data) {
                Music.hasNextPage = data.hasNextPage;
                $("#main table.list tbody").append(Music.renderData(data));

                if (Music.hasNextPage) {
                    $(window).bind("scroll", {url: url, options: options}, Music.loadOnScroll);
                }
                Music.infiniteScrollActive = false;
            }
        });
    },

    getOrderClass: function(field, data) {
        for (var key in data.order) {
            var item = data.order[key];
            if (item.field == field) {
                switch (item.direction) {
                    case "asc":
                        return " sort_asc";
                    case "desc":
                        return " sort_desc";
                }
            }
        }
        return "";
    },

    renderTable: function(data) {
        var html = "<table class=\"list\"><thead>";

        switch (data.type) {
            case "queue":
                html+= "<tr class=\"queue\">";
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"favourite_title sort_title" + Music.getOrderClass("title", data) + "\">" + gettext("Title") + "</th>";
                html+= "<th class=\"favourite_artist sort_artist" + Music.getOrderClass("artist", data) + "\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"favourite_album sort_album" + Music.getOrderClass("album", data) + "\">" + gettext("Album") + "</th>";
                html+= "<th class=\"favourite_genre sort_votes" + Music.getOrderClass("votes", data) + "\">" + gettext("Votes") + "</th>";
                html+= "<th class=\"favourite_added sort_created" + Music.getOrderClass("created", data) + "\">" + gettext("First voted") + "</th>";
                break;
            case "history":
                html+= "<tr class=\"history\">";
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"favourite_title sort_title" + Music.getOrderClass("title", data) + "\">" + gettext("Title") + "</th>";
                html+= "<th class=\"favourite_artist sort_artist" + Music.getOrderClass("artist", data) + "\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"favourite_album sort_album" + Music.getOrderClass("album", data) + "\">" + gettext("Album") + "</th>";
                html+= "<th class=\"favourite_genre sort_genre" + Music.getOrderClass("votes", data) + "\">" + gettext("Votes") + "</th>";
                html+= "<th class=\"favourite_added sort_created" + Music.getOrderClass("created", data) + "\">" + gettext("Date added") + "</th>";
                break;
            case "history/my":
                html+= "<tr class=\"history_my\">";
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"favourite_title sort_title" + Music.getOrderClass("title", data) + "\">" + gettext("Title") + "</th>";
                html+= "<th class=\"favourite_artist sort_artist" + Music.getOrderClass("artist", data) + "\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"favourite_album sort_album" + Music.getOrderClass("album", data) + "\">" + gettext("Album") + "</th>";
                html+= "<th class=\"favourite_genre sort_genre" + Music.getOrderClass("votes", data) + "\">" + gettext("Votes") + "</th>";
                html+= "<th class=\"favourite_added sort_created" + Music.getOrderClass("created", data) + "\">" + gettext("Date added") + "</th>";
                break;
            case "favourites":
                html+= "<tr class=\"favourites\">";
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"favourite_title sort_title" + Music.getOrderClass("title", data) + "\">" + gettext("Title") + "</th>";
                html+= "<th class=\"favourite_artist sort_artist" + Music.getOrderClass("artist", data) + "\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"favourite_album sort_album" + Music.getOrderClass("album", data) + "\">" + gettext("Album") + "</th>";
                html+= "<th class=\"favourite_genre sort_genre" + Music.getOrderClass("genre", data) + "\">" + gettext("Genre") + "</th>";
                html+= "<th class=\"favourite_added sort_created" + Music.getOrderClass("created", data) + "\">" + gettext("Date added") + "</th>";
                break;
            case "songs":
                html+= "<tr class=\"songs\">";
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"song_title sort_title" + Music.getOrderClass("title", data) + "\">" + gettext("Title") + "</th>";
                html+= "<th class=\"song_artist sort_artist" + Music.getOrderClass("artist", data) + "\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"song_album sort_album" + Music.getOrderClass("album", data) + "\">" + gettext("Album") + "</th>";
                html+= "<th class=\"song_genre sort_genre" + Music.getOrderClass("genre", data) + "\">" + gettext("Genre") + "</th>";
                html+= "<th class=\"song_year sort_year" + Music.getOrderClass("year", data) + "\">" + gettext("Year") + "</th>";
                html+= "<th class=\"song_length sort_length" + Music.getOrderClass("length", data) + "\">" + gettext("Length") + "</th>";
                break;
            case "artists":
                html+= "<tr class=\"artists\">";
                html+= "<th class=\"name sort_artist" + Music.getOrderClass("artist", data) + "\">" + gettext("Name") + "</th>";
                break;
            case "albums":
                html+= "<tr class=\"albums\">";
                html+= "<th class=\"album_title sort_album" + Music.getOrderClass("album", data) + "\">" + gettext("Title") + "</th>";
                html+= "<th class=\"album_artist sort_artist" + Music.getOrderClass("artist", data) + "\">" + gettext("Artist") + "</th>";
                break;
            case "genres":
                html+= "<tr class=\"genres\">";
                html+= "<th class=\"name sort_genre" + Music.getOrderClass("genre", data) + "\">" + gettext("Name") + "</th>";
                break;
            case "years":
                html+= "<tr class=\"years\">";
                html+= "<th class=\"year sort_year" + Music.getOrderClass("year", data) + "\">" + gettext("Year") + "</th>";
                break;
        }
        $(window).bind("scroll", {url: "/api/v1/" + data.type}, Music.loadOnScroll);
        html+= "</tr></thead><tbody></tbody></table>";

        return html;
    },

    renderData: function(data) {
        var html = "";
        $.each(data.itemList, function(index, item) {
            switch (data.type) {
                case "queue":
                    html+= "<tr class=\"row_queue\">";
                    html+= "<td>";
                    if (item.queued) {
                        html+= "<img src=\"/static/img/queue_active.png\" class=\"queue_remove\" data-id=\"" + item.id + "\" alt=\"" + gettext("Revoke vote") + "\" title=\"" + gettext("Revoke vote") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/queue.png\" class=\"queue_add\" data-id=\"" + item.id + "\" alt=\"" + gettext("Support vote") + "\" title=\"" + gettext("Support vote") + "\" />";
                    }
                    if (item.favourite) {
                        html+= "<img src=\"/static/img/favourite_active.png\" class=\"favourite_remove\" data-id=\"" + item.id + "\" alt=\"" + gettext("Remove from favourites") + "\" title=\"" + gettext("Remove from favourites") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/favourite.png\" class=\"favourite_add\" data-id=\"" + item.id + "\" alt=\"" + gettext("Add to favourites") + "\" title=\"" + gettext("Add to favourites") + "\" />";
                    }
                    html+= "</td>";

                    // title
                    if (item.title != null) {
                        html+= "<td class=\"filter search_title\" data-value=\"" + item.title + "\">" + item.title + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // artist
                    if (item.artist.id != null) {
                        html+= "<td class=\"filter filter_artist\" data-value=\"" + item.artist.id + "\">" + item.artist.name + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // album
                    if (item.album.id != null) {
                        html+= "<td class=\"filter filter_album\" data-value=\"" + item.album.id + "\">" + item.album.title + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    html+= "<td class=\"voteCount\">";
                    if (item.votes > 0) {
                        if (item.users.length == item.votes) {
                            html+= "<div class=\"voteTooltip\"><ul>";
                            for (var key in item.users) {
                                var user = item.users[key];
                                html+= "<li>" + user.name + "</li>"
                            }
                            html+= "</ul></div>";
                        }
                        html+= item.votes;
                    }
                    else {
                        html+= gettext("Autoplay");
                    }
                    html+= "</td>";

                    html+= "<td>" + item.created + "</td>";
                    break;
                case "history":
                case "history/my":
                    html+= "<tr class=\"row_history\">";
                    html+= "<td>";
                    if (item.queued) {
                        html+= "<img src=\"/static/img/queue_active.png\" class=\"queue_remove\" data-id=\"" + item.id + "\" alt=\"" + gettext("Revoke vote") + "\" title=\"" + gettext("Revoke vote") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/queue.png\" class=\"queue_add\" data-id=\"" + item.id + "\" alt=\"" + gettext("Vote to play") + "\" title=\"" + gettext("Vote to play") + "\" />";
                    }
                    if (item.favourite) {
                        html+= "<img src=\"/static/img/favourite_active.png\" class=\"favourite_remove\" data-id=\"" + item.id + "\" alt=\"" + gettext("Remove from favourites") + "\" title=\"" + gettext("Remove from favourites") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/favourite.png\" class=\"favourite_add\" data-id=\"" + item.id + "\" alt=\"" + gettext("Add to favourites") + "\" title=\"" + gettext("Add to favourites") + "\" />";
                    }
                    html+= "</td>";

                    // title
                    if (item.title != null) {
                        html+= "<td class=\"filter search_title\" data-value=\"" + item.title + "\">" + item.title + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // artist
                    if (item.artist.id != null) {
                        html+= "<td class=\"filter filter_artist\" data-value=\"" + item.artist.id + "\">" + item.artist.name + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // album
                    if (item.album.id != null) {
                        html+= "<td class=\"filter filter_album\" data-value=\"" + item.album.id + "\">" + item.album.title + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    html+= "<td class=\"voteCount\">";
                    if (item.votes > 0) {
                        if (item.users.length == item.votes) {
                            html+= "<div class=\"voteTooltip\"><ul>";
                            for (var key in item.users) {
                                var user = item.users[key];
                                html+= "<li>" + user.name + "</li>"
                            }
                            html+= "</ul></div>";
                        }
                        html+= item.votes;
                    }
                    else {
                        html+= gettext("Autoplay");
                    }
                    html+= "</td>";

                    html+= "<td>" + item.created + "</td>";
                    break;
                case "favourites":
                    html+= "<tr class=\"row_favourites\">";
                    html+= "<td>";
                    if (item.queued) {
                        html+= "<img src=\"/static/img/queue_active.png\" class=\"queue_remove\" data-id=\"" + item.id + "\" alt=\"" + gettext("Revoke vote") + "\" title=\"" + gettext("Revoke vote") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/queue.png\" class=\"queue_add\" data-id=\"" + item.id + "\" alt=\"" + gettext("Vote to play") + "\" title=\"" + gettext("Vote to play") + "\" />";
                    }
                    html+= "<img src=\"/static/img/favourite_active.png\" class=\"favourite_remove\" data-id=\"" + item.id + "\" alt=\"" + gettext("Remove from favourites") + "\" title=\"" + gettext("Remove from favourites") + "\" />";
                    html+= "</td>";

                    // title
                    if (item.title != null) {
                        html+= "<td class=\"filter search_title\" data-value=\"" + item.title + "\">" + item.title + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // artist
                    if (item.artist.id != null) {
                        html+= "<td class=\"filter filter_artist\" data-value=\"" + item.artist.id + "\">" + item.artist.name + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // album
                    if (item.album.id != null) {
                        html+= "<td class=\"filter filter_album\" data-value=\"" + item.album.id + "\">" + item.album.title + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // genre
                    if (item.genre.id != null) {
                        html+= "<td class=\"filter filter_genre\" data-value=\"" + item.genre.id + "\">" + item.genre.name + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    html+= "<td>" + item.created + "</td>";
                    break;
                case "songs":
                    html+= "<tr class=\"row_songs\">";
                    html+= "<td>";
                    if (item.queued) {
                        html+= "<img src=\"/static/img/queue_active.png\" class=\"queue_remove\" data-id=\"" + item.id + "\" alt=\"" + gettext("Revoke vote") + "\" title=\"" + gettext("Revoke vote") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/queue.png\" class=\"queue_add\" data-id=\"" + item.id + "\" alt=\"" + gettext("Vote to play") + "\" title=\"" + gettext("Vote to play") + "\" />";
                    }
                    if (item.favourite) {
                        html+= "<img src=\"/static/img/favourite_active.png\" class=\"favourite_remove\" data-id=\"" + item.id + "\" alt=\"" + gettext("Remove from favourites") + "\" title=\"" + gettext("Remove from favourites") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/favourite.png\" class=\"favourite_add\" data-id=\"" + item.id + "\" alt=\"" + gettext("Add to favourites") + "\" title=\"" + gettext("Add to favourites") + "\" />";
                    }
                    html+= "</td>";
                    // html+= "<td>" + ((item.title != null) ?  : "")  + "<span class=\"value invisible\">" + item.id + "</span></td>";

                    // title
                    if (item.title != null) {
                        html+= "<td class=\"filter search_title\" data-value=\"" + item.title + "\">" + item.title + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // artist
                    if (item.artist.id != null) {
                        html+= "<td class=\"filter filter_artist\" data-value=\"" + item.artist.id + "\">" + item.artist.name + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // album
                    if (item.album.id != null) {
                        html+= "<td class=\"filter filter_album\" data-value=\"" + item.album.id + "\">" + item.album.title + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // genre
                    if (item.genre.id != null) {
                        html+= "<td class=\"filter filter_genre\" data-value=\"" + item.genre.id + "\">" + item.genre.name + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // year
                    if (item.year != null) {
                        html+= "<td class=\"filter filter_year\" data-value=\"" + item.year + "\">" + item.year + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }

                    // length
                    var minutes = parseInt(item.length / 60);
                    var seconds = item.length % 60;
                    if (seconds < 10) {
                        seconds = "0" + seconds;
                    }
                    html+= "<td>" + minutes + ":" + seconds + "</td>";
                    break;
                case "artists":
                    html+= "<tr class=\"row_artists\">";
                    html+= "<td class=\"filter filter_artist\" data-value=\"" + item.id + "\">" + item.artist + "</td>";
                    break;
                case "albums":
                    html+= "<tr class=\"row_albums\">";
                    html+= "<td class=\"filter filter_album\" data-value=\"" + item.id + "\">" + item.album + "</td>";
                    if (item.artist.id != null) {
                        html+= "<td class=\"filter filter_artist\" data-value=\"" + item.artist.id + "\">" + item.artist.name + "</td>";
                    }
                    else {
                        html+= "<td>&#160;</td>";
                    }
                    break;
                case "genres":
                    html+= "<tr class=\"row_genres\">";
                    html+= "<td class=\"filter filter_genre\" data-value=\"" + item.id + "\">" + item.genre + "</td>";
                    break;
                case "years":
                    html+= "<tr class=\"row_years\">";
                    html+= "<td class=\"filter filter_year\" data-value=\"" + item.year + "\">" + item.year + "</td>";
                    break;
            }
            html+= "</tr>";
        });

        return html;
    }
};

$(document).ready(function() {
    Music.init();
});
