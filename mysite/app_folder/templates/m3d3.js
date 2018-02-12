var data_url = "http://127.0.0.1:5000/data";
$('#search').on('click', startSearch);

function startSearch() {
    var search_term = $("#search_term").prop('value');
    var limit_to = $('#limit_to').prop('value');
    getData(search_term, limit_to);
}

function getData(term, limit) {
  $.ajax({
    type: 'GET',
    async: true,
    timeout: 10000,
    url: data_url,
    data: {
        "term": term,
        "limit": limit,
    },
    dataType: 'json',
    beforeSend: function(xhr) {
      xhr.setRequestHeader('Accept', 'application/json, text/javascript, */*; q=0.01');
      xhr.setRequestHeader('Accept-Language', 'en-US,en;q=0.8');
      xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    },
    success: function(data) {
      var json_data = JSON.stringify(data);
      var search_data = JSON.parse(json_data).data;
      startForce(search_data);
  }
  });
}

function startForce(search_data) {
    var links = search_data;
    var nodes = {};

    // Compute the distinct nodes from the links.
    links.forEach(function(link) {
        link.source = nodes[link.source] || (nodes[link.source] = {
            name: link.source,
        });
        link.target = nodes[link.target] || (nodes[link.target] = {
            name: link.target,
        });
        link.value = +link.value;
    });

    var width = 500;
    var height = 500;

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([width, height])
        .linkDistance(25)
        .charge(-500)
        .on("tick", tick)
        .start();



    var link = svg.selectAll(".link")
        .data(force.links())
        .enter().append("line")
        .attr("class", "link");

    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", "node")

        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .on("click", click)
        .on("dblclick", dblclick)
        .call(force.drag);

    node.append("circle")
        .attr("r", 14)
        .style("fill", "#004BAF");


    node.append("text")
        .attr("x", 14)
        .attr("dy", ".35em")
        .style("fill", "#333")
        .text(function(d) {
            return d.name;
        });

    function tick() {
        link.attr("x1", function(d) {
                return d.source.x;
            })
            .attr("y1", function(d) {
                return d.source.y;
            })
            .attr("x2", function(d) {
                return d.target.x;
            })
            .attr("y2", function(d) {
                return d.target.y;
            });

        node.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    }

    function mouseover() {
        d3.select(this).select("circle").transition()
            .duration(750)
            .attr("r", 16);
    }

    function mouseout() {
        d3.select(this).select("circle").transition()
            .duration(750)
            .attr("r", 12);
    }
    // action to take on mouse click
    function click() {
        d3.select(this).select("text").transition()
            .duration(750)
            .attr("x", 22)
            .style("stroke-width", ".5px")
            .style("opacity", 1)
            .style("fill", "#E34A33")
            .style("font", "17.5px serif");
        d3.select(this).select("circle").transition()
            .duration(750)
            .style("fill", "#049FD9")
            .attr("r", 16);
    }

    // action to take on mouse double click
    function dblclick() {
        d3.select(this).select("circle").transition()
            .duration(750)
            .attr("r", 12)
            .style("fill", "#E34A33");
        d3.select(this).select("text").transition()
            .duration(750)
            .attr("x", 14)
            .style("stroke", "none")
            .style("fill", "#049FD9")
            .style("stroke", "none")
            .style("opacity", 0.6)
            .style("font", "14px serif");
    }
}
