if (typeof gettext != "function") {
    gettext = function(identifier) {
        return identifier;
    }
}

Music = {
    pageNum: 1,
    hasNextPage: true,
    infiniteScrollActive: false,
    sessionPing: 60000,
    csrf_token: null,

    init: function() {
        Music.csrf_token = $('#csrf_token input').val();

        $(".loadList").bind("click", function() {
            Music.setActiveMenu($(this));
            Music.loadList($(this).attr("href"));
            return false;
        });

        $("#searchform span.searchsubmit").bind("click", function() {
            Music.loadList("/api/v1/songs", {"search_term": $("input.searchterm").val()});
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            return false;
        });
        $("#searchform").bind("submit", function() {
            Music.loadList("/api/v1/songs", {"search_term": $("input.searchterm").val()});
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            return false;
        });

        $("#searchdetailsform span.searchsubmit").bind("click", function() {
            Music.loadList("/api/v1/songs", Music.getSearchOptions());
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            $("#searchoptions").click();
            return false;
        });
        $("#searchdetailsform").bind("submit", function() {
            Music.loadList("/api/v1/songs", Music.getSearchOptions());
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            $("#searchoptions").click();
            return false;
        });
        // chrome doesn't fire submit on #searchdetailsform -> dirty workaround
        $("#search_title, #search_artist, #search_album, #search_album").bind("keydown", function() {
            if (event.which == 13) {
                Music.loadList("/api/v1/songs", Music.getSearchOptions());
                Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
                $("#searchoptions").click();
                return false;
            }
        });

        $("#searchoptions").bind("click", function() {
            if ($("#searchdetails:visible").length == 1) {
                $(document).unbind("click.search");
                $("#searchdetails").hide();
                $("#search_title").val("");
                $("#search_artist").val("");
                $("#search_album").val("");
                $("#search_genre").find("option:selected").removeAttr("selected");
                $("#search_year").find("option:selected").removeAttr("selected");
            }
            else {
                $("#searchdetails").show();
                $(document).bind("click.search", function(event) {
                    if ($(event.target).closest("#searchdetails").length == 0 && $(event.target).closest("#searchoptions").length == 0) {
                        $("#searchoptions").click();
                    }
                });
            }
        });

        $("#main table.list img.filter").live("click", function() {
            var id = $(this).closest("tr").find(".value").html();
            if ($(this).hasClass("filter_artist")) {
                Music.loadList("/api/v1/songs", {"filter_artist_id": id});
            }
            else if ($(this).hasClass("filter_album")) {
                Music.loadList("/api/v1/songs", {"filter_album_id": id});
            }
            else if ($(this).hasClass("filter_genre")) {
                Music.loadList("/api/v1/songs", {"filter_genre": id});
            }
            else if ($(this).hasClass("filter_year")) {
                console.log($(this).parent("tr"));
                Music.loadList("/api/v1/songs", {"filter_year": id});
            }
            Music.setActiveMenu($("#sidebar ul li a.loadSongs"));
            return false;
        });

        $("#main table.list img.queue_add").live("click", function() {
            $.ajax({
                url: "/api/v1/queue",
                type: "POST",
                data: {
                    "id": $(this).closest("tr").find(".value").html(),
                    "csrfmiddlewaretoken": Music.csrf_token
                },
                success: function(data) {
                    var item = $("#queue_add_" + data.id);
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
                    var item = $("#queue_remove_" + data.id);
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
                    var item = $("#queue_remove_" + data.id);

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
                url: "/api/v1/queue/" + $(this).closest("tr").find(".value").html(),
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
                    "id": $(this).closest("tr").find(".value").html(),
                    "csrfmiddlewaretoken": Music.csrf_token
                },
                success: function(data) {
                    var item = $("#favourite_add_" + data.id);
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
                    var item = $("#favourite_remove_" + data.id);
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
                    var item = $("#favourite_remove_" + data.id);
                    item.closest("tr").fadeOut(1000, function() {
                        item.closest("tr").remove();
                    });
                };
            }

            $.ajax({
                url: "/api/v1/favourites/" + $(this).closest("tr").find(".value").html(),
                type: "DELETE",
                success: function(data) {
                    success(data);
                }
            });
            return false;
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

    loadList: function(url, options) {
        if (typeof options == "undefined") {
            options = {};
        }

        Music.pageNum = 1;
        Music.hasNextPage = false;

        // build options
        options.page = Music.pageNum;
        options.count = 30;

        $.ajax({
            url: url,
            data: options,
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

                // load data until page is populated
                if (Music.hasNextPage && Music.getScrollHeight() <= $(document).height()) {
                    $(window).unbind("scroll");
                    Music.loadItems(url, options);
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

    renderTable: function(data) {
        var html = "<table class=\"list\"><thead><tr>";
        switch (data.type) {
            case "queue":
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"favourite_title\">" + gettext("Title") + "</th>";
                html+= "<th class=\"favourite_artist\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"favourite_album\">" + gettext("Album") + "</th>";
                html+= "<th class=\"favourite_genre\">" + gettext("Votes") + "</th>";
                html+= "<th class=\"favourite_added\">" + gettext("First voted") + "</th>";
                break;
            case "history":
            case "history/my":
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"favourite_title\">" + gettext("Title") + "</th>";
                html+= "<th class=\"favourite_artist\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"favourite_album\">" + gettext("Album") + "</th>";
                html+= "<th class=\"favourite_genre\">" + gettext("Votes") + "</th>";
                html+= "<th class=\"favourite_added\">" + gettext("Date added") + "</th>";
                break;
            case "favourites":
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"favourite_title\">" + gettext("Title") + "</th>";
                html+= "<th class=\"favourite_artist\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"favourite_album\">" + gettext("Album") + "</th>";
                html+= "<th class=\"favourite_genre\">" + gettext("Genre") + "</th>";
                html+= "<th class=\"favourite_added\">" + gettext("Date added") + "</th>";
                break;
            case "songs":
                html+= "<th class=\"options\">&#160;</th>";
                html+= "<th class=\"song_title\">" + gettext("Title") + "</th>";
                html+= "<th class=\"song_artist\">" + gettext("Artist") + "</th>";
                html+= "<th class=\"song_album\">" + gettext("Album") + "</th>";
                html+= "<th class=\"song_genre\">" + gettext("Genre") + "</th>";
                html+= "<th class=\"song_year\">" + gettext("Year") + "</th>";
                html+= "<th class=\"song_length\">" + gettext("Length") + "</th>";
                break;
            case "artists":
                html+= "<th class=\"options_small\">&#160;</th>";
                html+= "<th class=\"name\">" + gettext("Name") + "</th>";
                break;
            case "albums":
                html+= "<th class=\"options_small\">&#160;</th>";
                html+= "<th class=\"album_title\">" + gettext("Title") + "</th>";
                html+= "<th class=\"album_artist\">" + gettext("Artist") + "</th>";
                break;
            case "genres":
                html+= "<th class=\"options_small\">&#160;</th>";
                html+= "<th class=\"name\">" + gettext("Name") + "</th>";
                break;
            case "years":
                html+= "<th class=\"options_small\">&#160;</th>";
                html+= "<th class=\"year\">" + gettext("Year") + "</th>";
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
                        html+= "<img src=\"/static/img/queue_active.png\" class=\"queue_remove\" id=\"queue_remove_" + item.id + "\" alt=\"" + gettext("Revoke vote") + "\" title=\"" + gettext("Revoke vote") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/queue.png\" class=\"queue_add\" id=\"queue_add_" + item.id + "\" alt=\"" + gettext("Support vote") + "\" title=\"" + gettext("Support vote") + "\" />";
                    }
                    if (item.favourite) {
                        html+= "<img src=\"/static/img/favourite_active.png\" class=\"favourite_remove\" id=\"favourite_remove_" + item.id + "\" alt=\"" + gettext("Remove from favourites") + "\" title=\"" + gettext("Remove from favourites") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/favourite.png\" class=\"favourite_add\" id=\"favourite_add_" + item.id + "\" alt=\"" + gettext("Add to favourites") + "\" title=\"" + gettext("Add to favourites") + "\" />";
                    }
                    html+= "</td>";
                    html+= "<td>" + ((item.title != null) ? item.title : "")  + "<span class=\"value invisible\">" + item.id + "</span></td>";
                    html+= "<td>" + ((item.artist.id != null) ? item.artist.name : "") + "</td>";
                    html+= "<td>" + ((item.album.id != null) ? item.album.title : "") + "</td>";
                    html+= "<td class=\"voteCount\">" + item.votes + "</td>";
                    html+= "<td>" + item.created + "</td>";
                    break;
                case "history":
                case "history/my":
                    html+= "<tr class=\"row_history\">";
                    html+= "<td>";
                    if (item.queued) {
                        html+= "<img src=\"/static/img/queue_active.png\" class=\"queue_remove\" id=\"queue_remove_" + item.id + "\" alt=\"" + gettext("Revoke vote") + "\" title=\"" + gettext("Revoke vote") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/queue.png\" class=\"queue_add\" id=\"queue_add_" + item.id + "\" alt=\"" + gettext("Vote to play") + "\" title=\"" + gettext("Vote to play") + "\" />";
                    }
                    if (item.favourite) {
                        html+= "<img src=\"/static/img/favourite_active.png\" class=\"favourite_remove\" id=\"favourite_remove_" + item.id + "\" alt=\"" + gettext("Remove from favourites") + "\" title=\"" + gettext("Remove from favourites") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/favourite.png\" class=\"favourite_add\" id=\"favourite_add_" + item.id + "\" alt=\"" + gettext("Add to favourites") + "\" title=\"" + gettext("Add to favourites") + "\" />";
                    }
                    html+= "</td>";
                    html+= "<td>" + ((item.title != null) ? item.title : "")  + "<span class=\"value invisible\">" + item.id + "</span></td>";
                    html+= "<td>" + ((item.artist.id != null) ? item.artist.name : "") + "</td>";
                    html+= "<td>" + ((item.album.id != null) ? item.album.title : "") + "</td>";
                    html+= "<td>" + ((item.votes > 0) ? item.votes : gettext("Autoplay")) + "</td>";
                    html+= "<td>" + item.created + "</td>";
                    break;
                case "favourites":
                    html+= "<tr class=\"row_favourites\">";
                    html+= "<td>";
                    if (item.queued) {
                        html+= "<img src=\"/static/img/queue_active.png\" class=\"queue_remove\" id=\"queue_remove_" + item.id + "\" alt=\"" + gettext("Revoke vote") + "\" title=\"" + gettext("Revoke vote") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/queue.png\" class=\"queue_add\" id=\"queue_add_" + item.id + "\" alt=\"" + gettext("Vote to play") + "\" title=\"" + gettext("Vote to play") + "\" />";
                    }
                    html+= "<img src=\"/static/img/favourite_active.png\" class=\"favourite_remove\" id=\"favourite_remove_" + item.id + "\" alt=\"" + gettext("Remove from favourites") + "\" title=\"" + gettext("Remove from favourites") + "\" />";
                    html+= "</td>";
                    html+= "<td>" + ((item.title != null) ? item.title : "")  + "<span class=\"value invisible\">" + item.id + "</span></td>";
                    html+= "<td>" + ((item.artist.id != null) ? item.artist.name : "") + "</td>";
                    html+= "<td>" + ((item.album.id != null) ? item.album.title : "") + "</td>";
                    html+= "<td>" + ((item.genre.id != null) ? item.genre.name : "") + "</td>";
                    html+= "<td>" + item.created + "</td>";
                    break;
                case "songs":
                    html+= "<tr class=\"row_songs\">";
                    html+= "<td>";
                    if (item.queued) {
                        html+= "<img src=\"/static/img/queue_active.png\" class=\"queue_remove\" id=\"queue_remove_" + item.id + "\" alt=\"" + gettext("Revoke vote") + "\" title=\"" + gettext("Revoke vote") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/queue.png\" class=\"queue_add\" id=\"queue_add_" + item.id + "\" alt=\"" + gettext("Vote to play") + "\" title=\"" + gettext("Vote to play") + "\" />";
                    }
                    if (item.favourite) {
                        html+= "<img src=\"/static/img/favourite_active.png\" class=\"favourite_remove\" id=\"favourite_remove_" + item.id + "\" alt=\"" + gettext("Remove from favourites") + "\" title=\"" + gettext("Remove from favourites") + "\" />";
                    }
                    else {
                        html+= "<img src=\"/static/img/favourite.png\" class=\"favourite_add\" id=\"favourite_add_" + item.id + "\" alt=\"" + gettext("Add to favourites") + "\" title=\"" + gettext("Add to favourites") + "\" />";
                    }
                    html+= "</td>";
                    html+= "<td>" + ((item.title != null) ? item.title : "")  + "<span class=\"value invisible\">" + item.id + "</span></td>";
                    html+= "<td>" + ((item.artist.id != null) ? item.artist.name : "") + "</td>";
                    html+= "<td>" + ((item.album.id != null) ? item.album.title : "") + "</td>";
                    html+= "<td>" + ((item.genre.id != null) ? item.genre.name : "") + "</td>";
                    html+= "<td>" + ((item.year != null) ? item.year : "") + "</td>";
                    var minutes = parseInt(item.length / 60);
                    var seconds = item.length % 60;
                    if (seconds < 10) {
                        seconds = "0" + seconds;
                    }
                    html+= "<td>" + minutes + ":" + seconds + "</td>";
                    break;
                case "artists":
                    html+= "<tr class=\"row_artists\">";
                    html+= "<td>";
                    html+= "<img src=\"/static/img/search.png\" class=\"filter filter_artist\" />";
                    html+= "</td>";
                    html+= "<td>" + item.artist + "<span class=\"value invisible\">" + item.id + "</span></td>";
                    break;
                case "albums":
                    html+= "<tr class=\"row_albums\">";
                    html+= "<td>";
                    html+= "<img src=\"/static/img/search.png\" class=\"filter filter_album\" />";
                    html+= "</td>";
                    html+= "<td>" + item.album + "<span class=\"value invisible\">" + item.id + "</span></td>";
                    html+= "<td>" + ((item.artist.id != null) ? item.artist.name : "") + "</td>";
                    break;
                case "genres":
                    html+= "<tr class=\"row_genres\">";
                    html+= "<td>";
                    html+= "<img src=\"/static/img/search.png\" class=\"filter filter_genre\" />";
                    html+= "</td>";
                    html+= "<td>" + item.genre + "<span class=\"value invisible\">" + item.id + "</span></td>";
                    break;
                case "years":
                    html+= "<tr class=\"row_years\">";
                    html+= "<td>";
                    html+= "<img src=\"/static/img/search.png\" class=\"filter filter_year\" />";
                    html+= "</td>";
                    html+= "<td class=\"value\">" + item.year + "</td>";
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
