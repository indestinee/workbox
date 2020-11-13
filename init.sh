dir=$(pwd)
cd ~/
unlink .vimrc
unlink .zshrc
unlink .zsh_aliases
ln -s $dir/vim/vimrc .vimrc
ln -s $dir/zsh/zshrc .zshrc
ln -s $dir/zsh/zsh_aliases .zsh_aliases

if [ ! -d .vim ]
then
    mkdir .vim
fi

cd .vim
unlink colors
unlink cpp_extend
unlink my-snippets

ln -s $dir/vim/colors .
ln -s $dir/vim/cpp_extend
ln -s $dir/vim/my-snippets
