function c = documentToA(keyToIndexMap, g, document)
    % Compute the column for a document
    l = zeros(length(keyToIndexMap), 1);
    
    % Find term frequencies for the document
    % Only find those that are supported by the precalculated g vector
    for j = 1:length(document)
        if isKey(keyToIndexMap, document{j})
            l(keyToIndexMap(document{j})) = l(keyToIndexMap(document{j})) + 1;
        end
    end
    % Column is the g value times the l value (Wikipedia)
    c = g .* log2(l + 1);
end

