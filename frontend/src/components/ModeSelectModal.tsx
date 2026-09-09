type Props = {
  onSelect: (mode: 'feed' | 'game') => void
}

export function ModeSelectModal({ onSelect }: Props) {
  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/60 px-4 animate-in fade-in duration-500">
      <div className="bg-zinc-900 border border-white/10 rounded-sm p-6 sm:p-8 w-full max-w-sm shadow-2xl flex flex-col gap-6" style={{ filter: 'url(#grain)' }}>
        <div className="flex flex-col gap-1">
          <h2 className="text-xl text-zinc-100" style={{ fontFamily: "'Fraunces', serif" }}>
            How do you want to explore?
          </h2>
          <p className="text-xs text-zinc-500">Pick a mode to get started.</p>
        </div>

        <div className="flex flex-col gap-3 -mt-3">
          <button
            onClick={() => onSelect('feed')}
            className="group flex flex-col gap-1 p-4 rounded-sm border border-white/10 hover:border-[#53131E] hover:bg-[#53131E]/10 transition-all text-left"
          >
            <span className="text-sm font-medium text-zinc-200">Feed</span>
            <span className="text-xs text-zinc-500 leading-relaxed">
              Browse all questions at once like a grid. Good for picking what catches your eye.
            </span>
          </button>

          <button
            onClick={() => onSelect('game')}
            className="group flex flex-col gap-1 p-4 rounded-sm border border-white/10 hover:border-[#53131E] hover:bg-[#53131E]/10 transition-all text-left"
          >
            <span className="text-sm font-medium text-zinc-200">Game Mode</span>
            <span className="text-xs text-zinc-500 leading-relaxed">
              Questions appear one at a time as swipeable cards. Good for taking turns with someone.
            </span>
          </button>
        </div>

        <p className="text-xs text-center -mt-3 -mb-2" style={{ color: '#53131E' }}>You can switch anytime from the bottom bar.</p>
      </div>
    </div>
  )
}
