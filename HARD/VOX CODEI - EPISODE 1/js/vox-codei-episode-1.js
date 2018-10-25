// https://www.codingame.com/ide/puzzle/vox-codei-episode-1
// https://github.com/Platane/Vox-Codei-codingame/blob/master/solution.js
/*
 * explosion pattern
 *
 *           x
 *           x
 *           x
 *     x x x b x x x
 *           x
 *           x
 *           x
 *   The explosion touch all the node as a cross pattern
 *
 *
 *
 *           #
 *     x x x b x #
 *           x
 *           x
 *           x
 *  The explosion does no traverse walls ( # ), but it traverse active node @
 *
 */


/**
 * @Class Map
 *
 * This object store a map as array and can manipulate it following th cg rules
 *
 * The stored map contains additionnal informations such as the bomb present in the map ( a bomb is a 'b' char ), and the active node which are already doomed because they will be destroyed by a ticking bomb.
 *
 * Tocking bomb are stored and will explode after 3 ticking method calls
 *
 * Can be instanciated using the global method readline
 * Can manipulate the node by simulating the cg rules ( bomb explosion )
 * Can extract the position where a bomb should be considered droped, and the dammage that it will do
 *
 */

var Map = function(){
    this.m = []
    this.bombs = []
}
Map.prototype = {

    /**
     * use readline global method to init the map, following the cg input structure
     */
    init : function(){

        var inputs = readline().split(' ')

        this.m.length = 0

        this.width = parseInt( inputs[0] )
        this.height = parseInt( inputs[1] )

        for (var i = this.height ; i-- ;)
            this.m.push(readline().split(''))

        return this

    },

    /**
     * make a bomb explode at the given position
     * replace the node by blank node on explosion patern
     * consider walls : do not change a node which is behind a wall
     */
    burst : function( x , y ){

        this.m[ y ][ x ] = '.'

        var m = this.m
        this._propage( x , y , function(x,y){
            m[ y ][ x ] = '.'
        })

        return this
    },

    /**
     * apply the explosion pattern, call the function passed in params on each node which is under the explosion pattern
     * @private
     */
    _propage : function( x , y , fn ){
        for( var dx=1 ; dx<=3 && x+dx < this.width && this.m[y][x+dx] != '#' ; dx ++)
            fn( x+dx , y )

        for( var dx=1 ; dx<=3 && x-dx >= 0 && this.m[y][x-dx] != '#' ; dx ++)
            fn( x-dx , y )

        for( var dy=1 ; dy<=3 && y+dy < this.height && this.m[y+dy][x] != '#' ; dy ++)
            fn( x , y+dy )

        for( var dy=1 ; dy<=3 && y-dy >= 0 && this.m[y-dy][x] != '#' ; dy ++)
            fn( x , y-dy )
    },

    /**
     * predict the damage that the bomb will cause,
     * the only valuable information is the number of nodes destroyed
     */
    predictDamages : function( x , y , fn ){

        var r = {
            nodes : [],
            bombs : [],
        }

        var m=this.m
        this._propage( x , y , function(x,y){
            switch( m[y][x] ){
                case '@' :
                    return r.nodes.push({x:x,y:y})

                case 'b' :
                    return r.bombs.push({x:x,y:y})
            }
        })

        return r
    },

    /**
     * return a list the position where the bomb will destroy at least one active node
     * the list is sorted, the first element destroy the most active node
     */
    extractValuablePosition : function(){

        var sites = []

        for(var x=this.width ; x-- ;)
        for(var y=this.height; y-- ;){

            if( this.m[y][x] != '.' )
                continue

            var r = this.predictDamages( x , y )

            if( r.nodes.length )
                sites.push({
                    x : x,
                    y : y,
                    f : r.nodes.length,
                    r : r
                })
        }

        return sites.sort( function(a,b){
            return a.f < b.f ? '1' : '-1'
        })
    },

    /**
     * make this node a deep copy of the node given in params
     */
    copy : function( m ){
        this.m.length=0
        this.bombs.length=0

        this.width = m.width
        this.height = m.height


        for (var i = this.height ; i-- ;)
            this.m.unshift( m.m[i].slice(0) )

        for (var i = m.bombs.length ; i-- ;)
            this.bombs.unshift({
                x : m.bombs[i].x,
                y : m.bombs[i].y,
                delay : m.bombs[i].delay,
            })

        return this
    },

    /**
     * return a deep copy of this node
     */
    clone : function(){
        return (new Map()).copy( this )
    },

    toString : function(){
        var buffer = []
        for( var k=this.m.length;k--;)
            buffer.unshift( this.m[k].join('') )

        return buffer.join('\n')
    },

    /**
     * place a bomb on the map
     * the bomb is stored in a array, in a ways that when the tick method is called x times, the burst method is call for the bomb
     */
    bomb : function( x , y , delay ){
        delay = typeof( delay ) == 'undefined' ? 3 : delay

        this.bombs.push({
            x:x,
            y:y,
            delay : delay
        })

        this.m[y][x] = 'b'

        var m = this.m
        this._propage( x , y , function(x,y){
            if( m[ y ][ x ] == '@' )
                m[ y ][ x ] = 'a'
        })

        return this
    },

    /**
     * declare that a round have passed, if one bomb have been here since 3 round, it explodes
     */
    tick : function(){
        for(var k=this.bombs.length;k--;)
            if( this.bombs[k].delay -- <= 0 ){
                this.burst( this.bombs[k].x , this.bombs[k].y )
                this.bombs.splice(k,1)
            }

        return this
    },

    /**
     * return the number of active node ( @ )
     */
    countNode : function(){
        var n=0
        for( var k=this.m.length;k--;)
        for( var i=this.m[k].length;i--;)
            if( this.m[k][i] == '@' )
                n++
        return n
    },
}

/**
 * given a starting state: a map a number of bombs and a number of rounds, return a list of command which leads to the destruction of all the nodes ( if it succeeds ).
 */
var solver = function( m0 , bombs , max ){

    /**
     * The algorithm is a simple "test and branch" algorithm
     *
     * starting from a state, all availables cmd are tested to generate the next states, iterate until a solution is found.
     * in fact, in order to limit the temporal complexity, only the more relevant command are tested :
     *  * the wait command ( do not place a bomb, just wait for the placed ones to explode )
     *  * place a bomb, at a clever position, do not consider a bomb position if the explosion does not destroy any active node. In fact, take only the first 3 position which destroy the more active nodes. This may not be suitable for all the case, but it does for the tests set.
     *
     * in order to found a solution fastly, evalue prioritly the most advanced stated ( the ones with the most rounds finished ) and evalue the 'wait' command the later.
     *
     *
     *
     * remark : the algorithm can be improve using a sort by heuristic
     *  a good heuritic could be
     *    * be small when there is a lot of 'wait' commands
     *    * be large when a lot of bomb will be destroyed
     */



    max = max || 99

    var openList = [{
        m : m0.clone(),
        nBombs : bombs,
        nNodes : m0.countNode(),
        cmd : [],

    }]

    while( openList.length ){

        // the current state, take the first of the list
        var s = openList.shift()

        // test state
        if( s.nNodes == 0 )
            break

        if( s.nBombs == 0 )
            continue

        if( s.cmd.length >= max )
            continue

        /////// PLACE A BOMB command

        // grab all the relevant position, sorted as the most effective ( in term of active node destruction )
        // take only the 3 first ones, which is enougth to pass the tests ( it limits the complexity )
        var ps = s.m.extractValuablePosition().slice(0,3)

        // for each relevant availables positions
        for( var k=ps.length;k--;){

            var m = s.m.clone()

            // place a bomb in the map
            .bomb( ps[k].x , ps[k].y )

            // update the ticking bomb ( eventually trigger the ones which have been place since 3 rounds )
            .tick()


            // push the new state, at the begining of the list, so it will be analyzed soon
            openList.unshift({

                m : m,

                nBombs : s.nBombs -1,

                nNodes : s.nNodes - ps[k].r.nodes.length,

                cmd : s.cmd.concat( [ ps[k].x+' '+ps[k].y ] )
            })
        }

        /////// WAIT command

        // push the new state, at the end of the list, so it will be analyzed after all the current ones
        openList.push({

            m : s.m.clone()

            // update the ticking bomb ( eventually trigger the ones which have been place since 3 rounds )
            .tick(),

            nBombs : s.nBombs,

            nNodes : s.nNodes,

            cmd : s.cmd.concat( [ 'WAIT' ] )
        })

    }

    return s.cmd
}

// init

var originalMap = ( new Map() ).init()

var cmd


// game loop
while (true) {


    var inputs

    if( !(inputs = readline() ) )
        break

    inputs = inputs.split(' ')




    var rounds = parseInt(inputs[0]); // number of rounds left before the end of the game
    var bombs = parseInt(inputs[1]); // number of bombs left

    if( !cmd )
        cmd = solver( originalMap , bombs , rounds )


    print( cmd.length ? cmd.shift() : 'WAIT' );
}