cda = (typeof(cda) === "undefined") ? {} : cda;

cda.serverurl = "http://localhost:8001/";
cda.service = {
    formatStr: function(str, args) {
        if (!args) { console.error("strFormat: args was empty for ", str); return; }

        return str.replace(/{(.*?)}/g,
            function (m, n) {
                var val = args[n];
                return (typeof val === "function") ? val() : val; 
        });
    },

    /* Use this to get foreign urls, makes things easy to refactor
     * @param endpoint: name mapping to a server endpoint (see switch statement)
     * @param params: necessary params to compute endpoint as a dictionary mapping
     *      param name to value
     * @param result: the URI for the endpoint on success, null on fail
     */
    geturl: function(endpoint, params) {
        var template = null;
        switch(endpoint) {
            case "grid":
                var x = params.x,
                    y = params.y;
                
                if (x && y) {
                    template = "grid/{x}/{y}/";
                }
                break;

            default:
                break;
        }

        return template ? cda.service.formatStr(cda.serverurl + template, params) : null;
    }
};
/* Returns true if x is null, undefined, or empty string
 */
cda.empty = function(x) {
    return typeof(x) === "undefined" || x === null || x === "";
};

OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {                
    defaultHandlerOptions: {
        'single': true,
        'double': false,
        'pixelTolerance': 0,
        'stopSingle': false,
        'stopDouble': false
    },
    
    initialize: function(options) {
        this.handlerOptions = OpenLayers.Util.extend(
            {}, this.defaultHandlerOptions
        );
        OpenLayers.Control.prototype.initialize.apply(
            this, arguments
        ); 
        this.handler = new OpenLayers.Handler.Click(
            this, {
                'click': this.trigger
            }, this.handlerOptions
        );
    }, 
    
    trigger: function(e) {
        var lonlat = map.getLonLatFromViewPortPx(e.xy);
        console.log({lon: lonlat.lon, lat: lonlat.lat});
        $("#coords").html("lon: " + lonlat.lon + ", lat: " + lonlat.lat);

        function geoToRect(lonlat){
            return {
                x: lonlat.lon,
                y: lonlat.lat
            }
        }

        var rect = geoToRect(lonlat);
        console.log(rect);

        var url = cda.service.geturl("grid", rect);
        var onSuccess = function(data, status, jqxhr) {
            console.debug(data);

            var table = $("<table></table>");
            table.append("<tr><th>Precipitation</th><th>Min Temp</th><th>Max Temp</th>" +
                         "<th>Year</th><th>Month</th><th>Day</th></tr>");
            var rows = data.data,
                header = data.header, 
                hm = {};

            for(var i = 0, len = header.length; i < len; i++) {
                name = header[i];
                hm[name] = i;
            }

            var precip_idx = hm.Precip, mint_idx = hm.Min_T, maxt_idx = hm.Max_T, date_idx = hm.Date;
            if (cda.empty(precip_idx) || cda.empty(mint_idx) || 
                cda.empty(maxt_idx) || cda.empty(date_idx)) {
                    table.append("<tr><td>Error: couldn't parse header!</td></tr>");
                    console.warn("Error: couldn't parse header!");
                    return;
            }

            for(var i = 0, len = rows.length; i < len; i++) {
                var value = rows[i], 
                    date = value[date_idx], 
                    day = date.substr(0, 2),
                    month = date.substr(2, 2),
                    year = date.substr(4, 4);
                table.append("<tr><td>" + value[precip_idx] + "</td><td>" + value[mint_idx] + "</td>"
                     + "<td>"+ value[maxt_idx] + "</td><td>" + year + "</td>"
                     + "<td>"+ month + "</td><td>"+ day + "</td></tr>");
            }

            $("#results table").empty().append(table);
        };

        var onFail = function(jqxhr, status, error) {
            console.debug(status);
            var table = $("<div>Error: server returned " + status + "!</div>");
            $("#results table").empty().append(table);
        };

        $.ajax({
            url: url,
            dataType: "json",
            method: "GET",
            success: onSuccess,
            error: onFail
        });
    }
});

var map;
function init() {
    map = new OpenLayers.Map('map');
    
    var ol_wms = new OpenLayers.Layer.WMS( "OpenLayers WMS",
                                           "http://vmap0.tiles.osgeo.org/wms/vmap0?", {layers: 'basic'} );
    
    var jpl_wms = new OpenLayers.Layer.WMS( "NASA Global Mosaic",
                                            "http://t1.hypercube.telascience.org/cgi-bin/landsat7", 
                                            {layers: "landsat7"});
    
    jpl_wms.setVisibility(false);

    map.addLayers([ol_wms, jpl_wms]);
    map.addControl(new OpenLayers.Control.LayerSwitcher());
    // map.setCenter(new OpenLayers.LonLat(0, 0), 0);
    map.zoomToMaxExtent();
    map.zoomIn();
    
    var click = new OpenLayers.Control.Click();
    map.addControl(click);
    click.activate();
}

$(document).ready(init);
