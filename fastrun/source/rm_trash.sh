trash_path=~/.Trash
logfile=~/.Trash/.logfile

if [ ! -d $trash_path ]
then
    mkdir $trash_path
fi

if [ ! -d $logfile ]
then
    mkdir $logfile
fi


timestamp=$(date "+%Y%m%d_%H%M%S_%s")
curpath=$(pwd -LP)

log=$logfile/$timestamp

cnt=0
for var in "$@"
do
    if [ -a "$var" ]
    then
        if [ $cnt = 0 ]
        then
            mkdir $trash_path/$timestamp
        fi

        echo $curpath $timestamp >> $log 
        mv "$var" $trash_path/$timestamp
        echo $var >> $log
        let cnt=$cnt+1
    fi
done


echo $cnt trash has moved to $trash_path/$timestamp, use ct to clean.

