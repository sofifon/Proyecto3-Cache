#### CACHE EN PRUEBAS HECHO POR FREDDY ZUNIGA 

import math
import gzip
import sys, getopt

#### FUNCION PARA OBTENER EL SIZE DEL OFFSET, INDEX Y TAG DEL CACHE
def get_size_offset_index_tag( ADDR_SIZE_BITS, CACHE_SIZE_KBYTES,
                               LINE_SIZE_BYTES, WAYS ):
    
    offset_size = int( math.log2( LINE_SIZE_BYTES ) )
    index_size = (2**10 * CACHE_SIZE_KBYTES) / (LINE_SIZE_BYTES * WAYS) 
    index_size = int( math.log2( index_size ) )
    tag_size = int( ADDR_SIZE_BITS - offset_size - index_size )

    return offset_size, index_size, tag_size

##### FUNCION PARA OBTENER LAS MASCARAS PARA PODER SACAR LOS VALORES DE
##### EL OFFSET, INDEX, Y TAG A PARTIR DE UNA DIRECCION 
def get_mask( sizes ):
    offset_mask = int( 2 ** sizes[0] - 1 )
    index_mask = int( 2 ** sizes[1] - 1 ) << sizes[0]
    tag_mask = int( 2 ** sizes[2] -1 ) << (sizes[0] + sizes[1])

    return offset_mask, index_mask, tag_mask

##### FUNCION PARA OBTENER LOS VALORES DEL OFFSET, INDEX Y TAG DE UNA DIRECCION
def get_offset_index_tag( addr, masks, sizes ):
    offset = ( addr & masks[0] )
    index = ( addr & masks[1] ) >>  sizes[0]
    tag = ( addr & masks[2] ) >> ( sizes[0] + sizes[1] )
    return offset, index, tag

def cache_init( index_bits, WAYS ):
    total_index = 2 ** index_bits
    ### cache and lru initialization in 0
    cache = [[[0 for metadata in range( 3 )] for way in range( WAYS )] for index in range( total_index )]
    return cache

def lru_init( index_bits, WAYS ):
    total_index = 2 ** index_bits
    lru = [[0 for way in range( WAYS )]for least in range( total_index )]
    return lru

def hit_detector( cache_index, WAYS, tag ):
    for w in range( WAYS ):
        hit = 0
        way = 0
        if( cache_index[w][0] == 1 and cache_index[w][2] == tag ):
            hit = 1
            way = w
            break
    return hit, way

def get_min_index( lru_index, WAYS ):
    minimum = lru_index[0]
    index = 0
    for k in range( 1, WAYS ):
        if( lru_index[k] < minimum ):
            minimum = lru_index[k]
            index = k
    return index, minimum

def get_max_index( lru_index, WAYS ):
    maximum = lru_index[0]
    index = 0
    for k in range( 1, WAYS ):
        if( lru_index[k] > maximum ):
            maximum = lru_index[k]
            index = k
    return index, maximum

def update_cache_lru( hit, way, index, lru, cache, ls, WAYS, tag ):
    min_index, min_value = get_min_index( lru[index], WAYS )
    max_index, max_value = get_max_index( lru[index], WAYS )
    if( hit == 0 ):
        lru[index][min_index] = max_value + 1
        cache[index][min_index][0] = 1
        cache[index][min_index][2] = tag
        if( ls == 1 ):
            cache[index][min_index][1] = 1
        else:
            cache[index][min_index][1] = 0
    else:
        if( lru[index][way] < max_value ):
            lru[index][way] = max_value + 1
        if( ls == 1 and cache[index][way][1] == 0):
            cache[index][way][1] = 1

            
##########################################################################
def main():

    help_text = "Be sure to use the next arguments when running the program \n -s f \n -a for asociativity"
    cache_size = 0
    cache_line_size = 0
    asociativity = 0
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "s:l:a:")
    except:
        print(help_text)

    for opt, arg in opts:
        if opt in ['-s']:
            CACHE_SIZE_KBYTES = int(arg)
        elif opt in ['-l']:
            LINE_SIZE_BYTES = int(arg)
        elif opt in ['-a']:
            WAYS = int(arg)
        else:
            print(help_text)

# do not run the program if one of the arguments is missing
    if 'CACHE_SIZE_KBYTES' not in locals() or 'LINE_SIZE_BYTES' not in locals() or 'WAYS' not in locals():
        print(help_text)
        sys.exit(2)

    ADDR_SIZE_BITS = 32 

    miss_count = 0
    hit_count = 0
    print (WAYS)

## sizes[0] = offset_bits, sizes[1] = index_bits, sizes[2] = tag_bits
    sizes = get_size_offset_index_tag( ADDR_SIZE_BITS, CACHE_SIZE_KBYTES,
                                   LINE_SIZE_BYTES, WAYS )
    masks = get_mask( sizes )

## INIT CACHE AND LRU TABLE
    cache = cache_init( sizes[1], WAYS )
    lru = lru_init( sizes[1], WAYS )

##########################################################################
###### aqui empezaria el trabajo de busqueda del cache
    hit_counter = 0
    miss_counter = 0
    replace_counter = 0

    trace = gzip.open( "mcf.trace.gz", "r" )

    while( 1 ):
        line = trace.readline()

        if( len( line ) == 0 ):
            break
    
        ls = int( line[2:3] )
        addr = int( line[4:12], 16 )
        ic = int( line[13:] )

        offset, index, tag = get_offset_index_tag( addr, masks, sizes)
        hit, way = hit_detector( cache[index], WAYS, tag )
        update_cache_lru( hit, way, index, lru, cache, ls, WAYS, tag )
        if( hit == 0 ):
            miss_counter += 1
            if ( ls == 0 ):
                replace_counter += 1
        else:
            hit_counter += 1


    trace.close()       
    print( "miss_counter = ", miss_counter )
    print( "hit_counter = ", hit_counter )
    print( "replace_counter =", replace_counter)

    hit_rate = hit_counter / (miss_counter + hit_counter )
    miss_rate = 1 - hit_rate

    print( "hit_rate:", hit_rate )
    print( "miss_rate:", miss_rate )

if __name__ == "__main__":
    main()
