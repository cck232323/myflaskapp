#!/bin/dash

# 检查参数数量是否正确
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <start> <end> <filename>"
    exit 1
fi

# 读取输入参数
start=$1
end=$2
filename=$3

# 使用shell内置的算术扩展来生成整数序列并写入文件
{
    while [ "$start" -le "$end" ]; do
        echo "$start"
        start=$((start + 1))
    done
} > "$filename"
