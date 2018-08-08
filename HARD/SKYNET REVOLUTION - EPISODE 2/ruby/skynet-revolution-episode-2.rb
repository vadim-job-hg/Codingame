STDOUT.sync = true # DO NOT REMOVE
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class SkyNetNetwork
  attr_accessor :total_nodes, :network, :gateways, :crit_nodes, :skynet_bot, :dijkstra, :distances, :paths

  def initialize
    # n: the total number of nodes in the level, including the gateways
    # l: the number of links
    # e: the number of exit gateways
    @total_nodes, total_links, total_gateways = gets.split(' ').collect {|x| x.to_i}
    @network = {}
    @gateways = {}
    @crit_nodes = {}
    @distances = {}
    @paths = {}

    build_links(total_links)
    build_gateways(total_gateways)
  end

  def run_round
    @skynet_bot = gets.to_i # The index of the node on which the Skynet agent is positioned this turn

    debug("DEBUG:: crit_nodes #{@crit_nodes}")
    debug("DEBUG:: network #{@network}")
    debug("DEBUG:: gateways #{@gateways}")

    debug('DEBUG:: under_pressure?')
    return if under_pressure?

    # Analyzing the most links to gateway
    find_distances_and_paths
    debug('DEBUG:: find_critical_pressure_for_gateways')
    return if find_critical_pressure_for_gateways

    # Before striking the shortest path, we need to find if a node is not in a critical position.
    # Take the farther node and check its shortest path. If, for each node, there's a pression,
    # we need to cut, if exists, the link from gateway to the node which owns the most links number to gateways
    debug('DEBUG:: find_pressure_for_all_gateways')
    return if find_pressure_for_all_gateways

    # If there's no more node link to more than 1 gateway, find the nearest node linked to the nearest gateway to cut this link

    debug('DEBUG:: cut_closest_link')
    cut_closest_link
  end

  private

  def build_links(total_links)
    total_links.times do
      # n1: N1 and N2 defines a link between these nodes
      n1, n2 = gets.split(' ').collect {|x| x.to_i}
      @network[n1] = {} unless @network[n1]
      @network[n2] = {} unless @network[n2]
      @network[n1][n2] = 1
      @network[n2][n1] = 1
      @network[n1][n1] = 0
      @network[n2][n2] = 0
    end
  end

  def build_gateways(total_gateways)
    total_gateways.times do
      ei = gets.to_i # the index of a gateway node
      @gateways[ei] = @network[ei];
      @gateways[ei].delete(ei)
      @network[ei] = {}
      @network[ei][ei] = 0

      @gateways[ei].each_key do |key|
        @crit_nodes[key] = 0 unless @crit_nodes[key]
        @crit_nodes[key] += 1
      end
    end
  end

  def cut_link(n1, n2)

    debug("DEBUG:: cut_link #{n1} #{n2}")

    @crit_nodes[n1] -= 1 if @crit_nodes[n1] && @crit_nodes[n1] > 0
    @crit_nodes[n2] -= 1 if @crit_nodes[n2] && @crit_nodes[n2] > 0

    @network[n1].delete(n1) if @network[n1] && @network[n1][n1]
    @network[n1].delete(n2) if @network[n1] && @network[n1][n2]
    @network[n2].delete(n1) if @network[n2] && @network[n2][n1]
    @network[n2].delete(n2) if @network[n2] && @network[n2][n2]

    @gateways[n2].delete(n1) if @gateways[n2] && @gateways[n2][n1]
    @gateways[n1].delete(n2) if @gateways[n1] && @gateways[n1][n2]

    # Example: 0 1 are the indices of the nodes you wish to sever the link between
    puts "#{n1} #{n2}"
    true
  end

  def under_pressure?
    @gateways.each do |gw_node, links|
      return cut_link(gw_node, @skynet_bot) if links.keys.include?(@skynet_bot)
    end
    false
  end

  def find_distances_and_paths(si = @skynet_bot)
    @dijkstra = Dijkstra.new(@network, @total_nodes)

    @gateways.keys.each do |gw_node|
      @dijkstra.find_shortest_path(si, gw_node)
      @distances[gw_node] = @dijkstra.distance(gw_node)
      debug("DEBUG:: DISTANCE gw #{gw_node}, distance #{@distances[gw_node]}")
      @paths[gw_node] = @dijkstra.shortest_path(gw_node)
      debug("DEBUG:: PATH gw #{gw_node}, paths #{@paths[gw_node]}")
    end
  end

  def find_critical_pressure_for_gateways

    @crit_nodes.each do |crit_node, crit_level|
      next if crit_level <= 1 #done  by under_pressure?
      @dijkstra.find_shortest_path(@skynet_bot, crit_node)
      path = @dijkstra.shortest_path(crit_node).reverse
      path.shift
      until path.empty? do
        analyzing_node = path.shift
        next if @crit_nodes[analyzing_node]
        # If there's a node which is not critical on the path, the critical level is reduced
        crit_level -= 1
      end
      # If this is not critical anymore, let's try another node
      next if crit_level <= 0

      # Otherwise, there'is a critical link to cut.
      @gateways.each do | gw_node, links |
        return cut_link(crit_node, gw_node) if links.keys.include? crit_node
      end
    end

    false
  end

  def find_pressure_for_all_gateways
    @distances.sort_by{|node, distance| distance}.to_h.keys.each do |gw_node|
      # Don't get the first node (SI) and the latest (GW)
      @paths[gw_node].each do |node_in_way|
        next if node_in_way == gw_node
        next if node_in_way == @skynet_bot
        unless @crit_nodes.key?(node_in_way)
          # If the gateway has a weak node (a node linked to another gateway), this node can be cut to prevent
          # impossible double cut at the same time action.
          weak_node = weak_node?(gw_node)
          debug("DEBUG:: cut_link weak #{gw_node} #{weak_node}");
          return cut_link(gw_node, weak_node) if weak_node != false
          break
        end
        debug("DEBUG:: cut_link all #{gw_node} #{node_in_way}");
        return cut_link(gw_node, node_in_way) if @crit_nodes[node_in_way] && @crit_nodes[node_in_way] > 1

      end
    end

    false
  end

  def weak_node?(gw_node_attacked)
    links_attacked = @gateways[gw_node_attacked]
    @gateways.each do |gw_node, links|
      next if gw_node == gw_node_attacked
      weak_nodes = links_attacked.keep_if{ |k, v| links.key? k }
      next if weak_nodes.empty?
      # If there's 1 weak node, return it to cut the link into this with its current gateway
      return weak_nodes.keys[0] if weak_nodes.size == 1

      # If there're severals weak nodes, Dijkstra them all and return the nearest
      min_dist = @total_nodes
      weakest_node = nil
      weak_nodes.keys.each do |weak_node|
        @dijkstra.find_shortest_path(@skynet_bot, weak_node)
        curr_dist = @dijkstra.distance(weak_node)
        if (min_dist > curr_dist)
          min_dist = curr_dist
          weakest_node = weak_node
        end
      end
      weakest_node
    end
    false
  end

  def cut_closest_link
    nearest_node = @distances.sort_by{|node, distance| distance}.to_h.keys[0]
    debug("DEBUG:: nearest_node #{nearest_node}")
    shortest_path = @paths[nearest_node]
    debug("DEBUG:: shortest_path #{shortest_path}")
    link_removed = shortest_path.last(2)
    debug("DEBUG:: link_removed #{link_removed}")
    node1, node2 = link_removed
    debug("DEBUG:: nodes #{node1} #{node2}")
    cut_link(node1, node2)
  end

  def debug(msg)
    # STDERR.puts msg
  end
end

class Dijkstra
  attr_accessor :visited, :distance, :previous_node, :start_node, :map, :infinite_distance, :number_of_nodes, :best_node, :matrix_width

  def initialize(map, infinite_distance)
    @map = map
    @infinite_distance = infinite_distance
    @number_of_nodes = @map.size
    @best_node = 0
    @matrix_width = 0
    @visited = {}
    @distance = {}
    @previous_node = {}
  end

  def find_shortest_path(start, to = nil)
    @start_node = start
    @map.each do |node, links|
      if node == @start_node
        @visited[node] = true
        @distance[node] = 0
      else
        @visited[node] = false
        @distance[node] = @infinite_distance
        @distance[node] = @map[@start_node][node] if @map[@start_node] and @map[@start_node][node]
      end
      @previous_node[node] = @start_node
    end

    tries = 0

    while @visited.values.include?(false) and tries <= @number_of_nodes do
      nodes_left = @visited.reject{ |node, visited| visited == true }.keys
      @best_node = find_best_node(@distance, nodes_left)
      break if to && to == @best_node

      update_distance_and_previous(best_node)
      @visited[best_node] = true
      tries += 1
    end
  end

  def find_best_node(distance, nodes_left)
    best_path = @infinite_distance
    best_node = nil
    nodes_left.each do |node|
      if distance[node] < best_path
        best_path = distance[node]
        best_node = node
      end
    end
    best_node
  end

  def update_distance_and_previous(best_node)
    @map.each do |node, links|

      if @map[best_node] &&
          @map[best_node][node] &&
          (@map[best_node][node] != @infinite_distance || @map[best_node][node] == 0) &&
          (@distance[best_node] + @map[best_node][node]) < @distance[node]

        @distance[node] = @distance[best_node] + @map[best_node][node]
        @previous_node[node] = best_node
      end
    end
  end

  def distance(to)
    @distance[to]
  end

  def shortest_path(to = nil)
    shortest_path = {}
    @map.each do |node, link|
      next if to != node and not to.nil?
      shortest_path[node] = []
      end_node = nil
      curr_node = node
      shortest_path[node] << node
      while end_node.nil? or end_node != @start_node do
        shortest_path[node] << @previous_node[curr_node]
        end_node = @previous_node[curr_node]
        curr_node = @previous_node[curr_node]
      end
      shortest_path[node] = shortest_path[node].reverse

      if to.nil? || to == node
        if @distance[node] >= @infinite_distance
          shortest_path[node].clear
          next
        end
        break if to == node
      end
    end

    return shortest_path if to.nil?

    return shortest_path[to] if shortest_path[to]

    []
  end

  def debug(msg)
    # STDERR.puts msg
  end
end

@sky_net = SkyNetNetwork.new

# game loop
loop do
  @sky_net.run_round
end
