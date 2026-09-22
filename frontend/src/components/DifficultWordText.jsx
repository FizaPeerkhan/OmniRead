import { useMemo } from 'react';

export default function DifficultWordText({ text, difficultWords, onSelect }) {
  const parts = useMemo(() => {
    if (!text || !Array.isArray(difficultWords) || difficultWords.length === 0) return [{ text, word: null }];

    const ranges = difficultWords
      .map((item, index) => ({ ...item, _index: index, start: Number(item.start), end: Number(item.end) }))
      .filter((item) => Number.isFinite(item.start) && Number.isFinite(item.end) && item.start >= 0 && item.end > item.start && item.end <= text.length)
      .sort((a, b) => a.start - b.start);

    const output = [];
    let cursor = 0;
    for (const item of ranges) {
      if (item.start < cursor) continue;
      if (item.start > cursor) output.push({ text: text.slice(cursor, item.start), word: null });
      output.push({ text: text.slice(item.start, item.end), word: item });
      cursor = item.end;
    }
    if (cursor < text.length) output.push({ text: text.slice(cursor), word: null });
    return output;
  }, [text, difficultWords]);

  return (
    <div className="reading-text whitespace-pre-wrap text-[1.05rem] text-slate-700">
      {parts.map((part, index) => part.word ? (
        <button
          key={`${part.word.word}-${part.word.start}-${index}`}
          type="button"
          className="difficult-word"
          title="Select for difficulty details"
          onClick={() => onSelect(part.word)}
        >
          {part.text}
        </button>
      ) : <span key={index}>{part.text}</span>)}
    </div>
  );
}
