/**
 * Teaching Session Component
 * Displays 8-section Goku-style teaching with streaming text and audio
 */
'use client';

import { useState, useEffect, useRef } from 'react';
import { useTeachingStream, useTypewriter } from '@/lib/useStreaming';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';

interface TeachingSessionProps {
  conceptId: string;
  conceptName: string;
  onComplete?: () => void;
}

const SECTION_METADATA = {
  hook: { title: 'Why This Matters', icon: '🎯', color: 'bg-amber-500' },
  analogy: { title: 'Real-World Comparison', icon: '🌍', color: 'bg-blue-500' },
  core: { title: 'The Core Concept', icon: '💡', color: 'bg-purple-500' },
  visual: { title: 'Picture This', icon: '🎨', color: 'bg-pink-500' },
  example: { title: 'Concrete Example', icon: '📝', color: 'bg-green-500' },
  mistake: { title: 'Common Pitfall', icon: '⚠️', color: 'bg-red-500' },
  practice: { title: 'Think About This', icon: '🤔', color: 'bg-indigo-500' },
  encouragement: { title: 'You Got This!', icon: '💪', color: 'bg-orange-500' },
};

export function TeachingSession({ conceptId, conceptName, onComplete }: TeachingSessionProps) {
  const { sections, currentSection, audioUrls, progress, done, error, isStreaming } =
    useTeachingStream(conceptId);

  const [activeSection, setActiveSection] = useState<string | null>(null);
  const [completedSections, setCompletedSections] = useState<Set<string>>(new Set());
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Update active section when streaming changes
  useEffect(() => {
    if (currentSection && currentSection !== activeSection) {
      setActiveSection(currentSection);
    }
  }, [currentSection, activeSection]);

  // Mark section as complete when it finishes
  useEffect(() => {
    if (activeSection && sections[activeSection] && !isStreaming) {
      setCompletedSections((prev) => new Set(prev).add(activeSection));
    }
  }, [activeSection, sections, isStreaming]);

  // Handle session completion
  useEffect(() => {
    if (done && onComplete) {
      onComplete();
    }
  }, [done, onComplete]);

  const playAudio = (sectionName: string) => {
    const audioUrl = audioUrls[sectionName];
    if (!audioUrl) return;

    if (audioRef.current) {
      audioRef.current.pause();
    }

    audioRef.current = new Audio(audioUrl);
    audioRef.current.play();
    setIsPlaying(true);

    audioRef.current.onended = () => {
      setIsPlaying(false);
    };
  };

  const pauseAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  const nextSection = () => {
    const sectionOrder = Object.keys(SECTION_METADATA);
    const currentIndex = activeSection ? sectionOrder.indexOf(activeSection) : -1;
    if (currentIndex < sectionOrder.length - 1) {
      const next = sectionOrder[currentIndex + 1];
      setActiveSection(next);
    }
  };

  if (error) {
    return (
      <Card className="p-6 border-red-500">
        <div className="text-red-600">
          <h3 className="text-lg font-bold mb-2">Error</h3>
          <p>{error}</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Learning: {conceptName}
        </h1>
        <div className="flex items-center justify-center gap-4">
          <Progress value={parseInt(progress.split('/')[0]) * 12.5} className="w-64" />
          <span className="text-sm text-gray-600 dark:text-gray-400">{progress}</span>
        </div>
      </div>

      {/* Goku Avatar */}
      <div className="flex justify-center">
        <div
          className={`w-24 h-24 rounded-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center text-4xl transition-transform ${
            isStreaming ? 'animate-bounce' : ''
          }`}
        >
          🥋
        </div>
      </div>

      {/* Section Cards */}
      <div className="space-y-4">
        {Object.entries(SECTION_METADATA).map(([sectionKey, metadata]) => {
          const sectionText = sections[sectionKey] || '';
          const isActive = activeSection === sectionKey;
          const isComplete = completedSections.has(sectionKey);
          const hasAudio = !!audioUrls[sectionKey];

          if (!sectionText && !isActive) return null;

          return (
            <SectionCard
              key={sectionKey}
              sectionKey={sectionKey}
              metadata={metadata}
              text={sectionText}
              isActive={isActive}
              isComplete={isComplete}
              hasAudio={hasAudio}
              isPlaying={isPlaying && activeSection === sectionKey}
              onPlayAudio={() => playAudio(sectionKey)}
              onPauseAudio={pauseAudio}
            />
          );
        })}
      </div>

      {/* Navigation */}
      {activeSection && !isStreaming && (
        <div className="flex justify-center gap-4">
          <Button onClick={nextSection} size="lg" className="bg-orange-500 hover:bg-orange-600">
            Next Section →
          </Button>
        </div>
      )}

      {/* Completion */}
      {done && (
        <Card className="p-6 bg-gradient-to-r from-green-500 to-emerald-500 text-white">
          <div className="text-center space-y-2">
            <div className="text-4xl">🎉</div>
            <h3 className="text-2xl font-bold">Awesome Work!</h3>
            <p>You've completed the teaching session. Ready for some practice?</p>
            <Button
              onClick={onComplete}
              size="lg"
              className="bg-white text-green-600 hover:bg-gray-100"
            >
              Start Quiz
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}

interface SectionCardProps {
  sectionKey: string;
  metadata: { title: string; icon: string; color: string };
  text: string;
  isActive: boolean;
  isComplete: boolean;
  hasAudio: boolean;
  isPlaying: boolean;
  onPlayAudio: () => void;
  onPauseAudio: () => void;
}

function SectionCard({
  metadata,
  text,
  isActive,
  isComplete,
  hasAudio,
  isPlaying,
  onPlayAudio,
  onPauseAudio,
}: SectionCardProps) {
  const { displayText, isTyping } = useTypewriter(text, 20);

  return (
    <Card
      className={`p-6 transition-all duration-300 ${
        isActive ? 'ring-2 ring-orange-500 shadow-lg scale-105' : ''
      } ${isComplete ? 'opacity-90' : ''}`}
    >
      <div className="space-y-4">
        {/* Section Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className={`w-12 h-12 rounded-full ${metadata.color} flex items-center justify-center text-2xl`}
            >
              {metadata.icon}
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                {metadata.title}
              </h3>
              {isComplete && (
                <span className="text-sm text-green-600 dark:text-green-400">✓ Complete</span>
              )}
            </div>
          </div>

          {/* Audio Controls */}
          {hasAudio && (
            <Button
              onClick={isPlaying ? onPauseAudio : onPlayAudio}
              variant="outline"
              size="sm"
              className="gap-2"
            >
              {isPlaying ? '⏸️ Pause' : '🔊 Play Audio'}
            </Button>
          )}
        </div>

        {/* Section Content */}
        <div className="prose dark:prose-invert max-w-none">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {displayText}
            {isTyping && <span className="animate-pulse">▊</span>}
          </p>
        </div>

        {/* Key Terms Highlight */}
        {isActive && (
          <div className="flex flex-wrap gap-2">
            {extractKeyTerms(text).map((term, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-200 rounded-full text-sm font-medium animate-pulse"
              >
                {term}
              </span>
            ))}
          </div>
        )}
      </div>
    </Card>
  );
}

function extractKeyTerms(text: string): string[] {
  // Simple extraction - look for capitalized words or quoted terms
  const terms: string[] = [];
  const capitalizedWords = text.match(/\b[A-Z][a-z]+\b/g) || [];
  const quotedTerms = text.match(/"([^"]+)"/g) || [];

  terms.push(...capitalizedWords.slice(0, 3));
  terms.push(...quotedTerms.map((t) => t.replace(/"/g, '')).slice(0, 2));

  return [...new Set(terms)].slice(0, 5);
}

// Made with Bob
