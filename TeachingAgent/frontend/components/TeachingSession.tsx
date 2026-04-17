/**
 * Teaching Session Component - Redesigned
 * Modern UI with section navigation, progress tracking, and flashcard integration
 */
'use client';

import { useState, useEffect, useRef } from 'react';
import { useTeachingStream } from '@/lib/useStreaming';
import { Card, CardTitle, CardText } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, ArrowRight, CheckCircle2, Circle, BookOpen, Brain, Zap, Target, Award, Volume2, VolumeX } from 'lucide-react';
import { FlashcardDeck } from '@/components/FlashcardDeck';

interface TeachingSessionProps {
  conceptId: string;
  conceptName: string;
  onComplete?: () => void;
}

const SECTION_METADATA = {
  hook: { title: 'Exam Importance', icon: '🎯', color: 'from-amber-500 to-orange-500', description: 'Why this matters for exams' },
  analogy: { title: 'Technical Comparison', icon: '🔄', color: 'from-blue-500 to-cyan-500', description: 'Compare with related concepts' },
  core: { title: 'Core Definition', icon: '💡', color: 'from-purple-500 to-pink-500', description: 'Precise technical explanation' },
  visual: { title: 'Architecture', icon: '🏗️', color: 'from-green-500 to-emerald-500', description: 'Structure and components' },
  example: { title: 'Technical Example', icon: '📝', color: 'from-indigo-500 to-purple-500', description: 'Detailed walkthrough' },
  mistake: { title: 'Common Exam Mistake', icon: '⚠️', color: 'from-red-500 to-pink-500', description: 'What to avoid' },
  practice: { title: 'PYQ Scenario', icon: '🤔', color: 'from-teal-500 to-cyan-500', description: 'Practice question' },
  encouragement: { title: 'Exam Strategy', icon: '💪', color: 'from-orange-500 to-red-500', description: 'Key points summary' },
};

type SectionName = keyof typeof SECTION_METADATA;

export function TeachingSession({ conceptId, conceptName, onComplete }: TeachingSessionProps) {
  const { sections, currentSection, audioUrls, progress, done, error, isStreaming } =
    useTeachingStream(conceptId);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [completedSections, setCompletedSections] = useState<Set<string>>(new Set());
  const [showFlashcards, setShowFlashcards] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [flashcards, setFlashcards] = useState<any[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Fetch flashcards when session completes
  useEffect(() => {
    if (done && !flashcards.length) {
      fetch(`http://localhost:8000/api/concepts/${conceptId}/flashcards`)
        .then(res => res.json())
        .then(data => setFlashcards(data || []))
        .catch(err => console.error('Failed to load flashcards:', err));
    }
  }, [done, conceptId, flashcards.length]);

  const sectionOrder: SectionName[] = ['hook', 'analogy', 'core', 'visual', 'example', 'mistake', 'practice', 'encouragement'];
  const currentSectionName = sectionOrder[currentIndex];
  const currentSectionData = sections[currentSectionName] || '';
  const totalSections = sectionOrder.length;
  const progressPercent = ((currentIndex + 1) / totalSections) * 100;

  // Mark section as complete when content arrives
  useEffect(() => {
    if (currentSectionData && !isStreaming) {
      setCompletedSections((prev) => new Set(prev).add(currentSectionName));
    }
  }, [currentSectionData, isStreaming, currentSectionName]);

  // Auto-advance when section completes
  useEffect(() => {
    if (done && currentIndex < totalSections - 1) {
      // All sections loaded, can navigate freely
    }
  }, [done, currentIndex, totalSections]);

  const nextSection = () => {
    if (currentIndex < totalSections - 1) {
      setCurrentIndex(currentIndex + 1);
    } else if (done) {
      setShowFlashcards(true);
    }
  };

  const prevSection = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const goToSection = (index: number) => {
    setCurrentIndex(index);
  };

  const playAudio = (sectionName: string) => {
    const audioUrl = audioUrls[sectionName];
    if (!audioUrl) return;

    if (audioRef.current) {
      audioRef.current.pause();
    }

    const fullAudioUrl = audioUrl.startsWith('http') 
      ? audioUrl 
      : `http://localhost:8000${audioUrl}`;
    
    audioRef.current = new Audio(fullAudioUrl);
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

  if (showFlashcards) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
        <div className="max-w-4xl mx-auto">
          <Button
            onClick={() => setShowFlashcards(false)}
            variant="ghost"
            className="mb-4 text-slate-300 hover:text-white"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Teaching
          </Button>
          <FlashcardDeck
            cards={flashcards}
            onCardReview={(cardId, quality) => {
              console.log('Card reviewed:', cardId, quality);
            }}
            onComplete={onComplete}
          />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-6">
        <Card className="max-w-md bg-red-900/20 border-red-500/50">
          <div className="p-6 text-center">
            <div className="text-4xl mb-4">⚠️</div>
            <CardTitle className="text-red-400 mb-2">Error Loading Session</CardTitle>
            <CardText className="text-red-300">{error}</CardText>
            <Button onClick={onComplete} className="mt-4" variant="danger">
              Go Back
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  const metadata = SECTION_METADATA[currentSectionName];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <Button
            onClick={onComplete}
            variant="ghost"
            className="text-slate-300 hover:text-white"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Concepts
          </Button>
          <div className="text-right">
            <div className="text-sm text-slate-400">Learning</div>
            <div className="text-lg font-bold text-white">{conceptName}</div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-slate-300">
              Section {currentIndex + 1} of {totalSections}
            </span>
            <span className="text-sm font-medium text-purple-400">
              {Math.round(progressPercent)}% Complete
            </span>
          </div>
          <Progress value={progressPercent} className="h-2 bg-slate-800" />
        </div>

        {/* Section Navigation Pills */}
        <div className="flex flex-wrap gap-2 mb-6">
          {sectionOrder.map((section, idx) => {
            const meta = SECTION_METADATA[section];
            const isCompleted = completedSections.has(section);
            const isCurrent = idx === currentIndex;
            
            return (
              <button
                key={section}
                onClick={() => goToSection(idx)}
                className={`
                  flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all
                  ${isCurrent 
                    ? 'bg-gradient-to-r ' + meta.color + ' text-white shadow-lg scale-105' 
                    : isCompleted
                    ? 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                    : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                  }
                `}
                disabled={!isCompleted && !isCurrent}
              >
                {isCompleted ? (
                  <CheckCircle2 className="w-4 h-4" />
                ) : (
                  <Circle className="w-4 h-4" />
                )}
                <span>{meta.icon}</span>
                <span className="hidden sm:inline">{meta.title}</span>
              </button>
            );
          })}
        </div>

        {/* Main Content Card */}
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700 shadow-2xl mb-6">
          <div className="p-8">
            {/* Section Header */}
            <div className="flex items-start justify-between mb-6">
              <div>
                <div className={`inline-block px-4 py-2 rounded-lg bg-gradient-to-r ${metadata.color} text-white font-bold text-lg mb-2`}>
                  {metadata.icon} {metadata.title}
                </div>
                <p className="text-slate-400 text-sm">{metadata.description}</p>
              </div>
              {audioUrls[currentSectionName] && (
                <Button
                  onClick={() => isPlaying ? pauseAudio() : playAudio(currentSectionName)}
                  variant="ghost"
                  className="text-purple-400 hover:text-purple-300"
                >
                  {isPlaying ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
                </Button>
              )}
            </div>

            {/* Content */}
            <div className="prose prose-invert max-w-none">
              {currentSectionData ? (
                <p className="text-slate-200 text-lg leading-relaxed whitespace-pre-wrap">
                  {currentSectionData}
                  {isStreaming && currentSection === currentSectionName && (
                    <span className="inline-block w-2 h-5 bg-purple-500 ml-1 animate-pulse" />
                  )}
                </p>
              ) : (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Loading section...</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </Card>

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between">
          <Button
            onClick={prevSection}
            disabled={currentIndex === 0}
            variant="ghost"
            className="text-slate-300 hover:text-white disabled:opacity-30"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Previous
          </Button>

          <div className="flex gap-3">
            {currentIndex === totalSections - 1 && done ? (
              <Button
                onClick={() => setShowFlashcards(true)}
                className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white shadow-lg"
              >
                <Brain className="w-4 h-4 mr-2" />
                Practice with Flashcards
              </Button>
            ) : (
              <Button
                onClick={nextSection}
                disabled={!currentSectionData || (currentIndex === totalSections - 1 && !done)}
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg disabled:opacity-30"
              >
                Next Section
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            )}
          </div>
        </div>

        {/* Stats Footer */}
        <div className="mt-8 grid grid-cols-3 gap-4">
          <Card className="bg-slate-800/30 border-slate-700 p-4 text-center">
            <div className="text-2xl font-bold text-purple-400">{completedSections.size}</div>
            <div className="text-sm text-slate-400">Sections Completed</div>
          </Card>
          <Card className="bg-slate-800/30 border-slate-700 p-4 text-center">
            <div className="text-2xl font-bold text-blue-400">{totalSections - completedSections.size}</div>
            <div className="text-sm text-slate-400">Remaining</div>
          </Card>
          <Card className="bg-slate-800/30 border-slate-700 p-4 text-center">
            <div className="text-2xl font-bold text-green-400">{Math.round(progressPercent)}%</div>
            <div className="text-sm text-slate-400">Progress</div>
          </Card>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
