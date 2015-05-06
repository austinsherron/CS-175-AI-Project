function addToMap( map, word )
    if ~isKey(map, word)
        map(word) = 1;
    else
        map(word) = map(word) + 1;
    end
end

