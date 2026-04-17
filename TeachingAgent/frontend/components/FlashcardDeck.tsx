/**
 * Flashcard Deck Component
 * Swipeable flashcards with SM-2 spaced repetition
 */
'use client';

import { useState, useRef, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface Flashcard {
  id: string;
  front: string;
  back: string;
  cue: string;
}

interface FlashcardDeckProps {
  cards: Flashcard[];
  onCardReview: (cardId: string, quality: number) => void;
  onComplete?: () => void;
}

export function FlashcardDeck({ cards, onCardReview, onComplete }: FlashcardDeckProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [streak, setStreak] = useState(0);
  const [reviewedCards, setReviewedCards] = useState<Set<string>>(new Set());

  const currentCard = cards[currentIndex];
  const progress = ((currentIndex + 1) / cards.length) * 100;

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
  };

  const handleReview = (quality: number) => {
    if (!currentCard) return;

    // Record review
    onCardReview(currentCard.id, quality);
    setReviewedCards((prev) => new Set(prev).add(currentCard.id));

    // Update streak
    if (quality >= 3) {
      setStreak((prev) => prev + 1);
    } else {
      setStreak(0);
    }

    // Move to next card
    if (currentIndex < cards.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setIsFlipped(false);
    } else if (onComplete) {
      onComplete();
    }
  };

  if (!currentCard) {
    return (
      <Card className="p-8 text-center">
        <div className="space-y-4">
          <div className="text-6xl">🎉</div>
          <h2 className="text-2xl font-bold">Deck Complete!</h2>
          <p className="text-gray-600 dark:text-gray-400">
            You reviewed {reviewedCards.size} cards
          </p>
          {streak > 0 && (
            <p className="text-lg font-semibold text-green-600">
              Final streak: {streak} 🔥
            </p>
          )}
        </div>
      </Card>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Progress */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400">
          <span>
            Card {currentIndex + 1} of {cards.length}
          </span>
          {streak > 0 && <span className="text-orange-500 font-semibold">{streak} 🔥</span>}
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            className="bg-gradient-to-r from-orange-500 to-red-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Flashcard */}
      <FlashcardView
        card={currentCard}
        isFlipped={isFlipped}
        onFlip={handleFlip}
        onSwipeLeft={() => handleReview(0)}
        onSwipeRight={() => handleReview(5)}
      />

      {/* Controls */}
      {isFlipped && (
        <div className="grid grid-cols-5 gap-2">
          <Button
            onClick={() => handleReview(0)}
            variant="danger"
            className="col-span-1"
          >
            ✗
          </Button>
          <Button
            onClick={() => handleReview(2)}
            variant="ghost"
            className="col-span-1"
          >
            Hard
          </Button>
          <Button
            onClick={() => handleReview(3)}
            variant="ghost"
            className="col-span-1"
          >
            Good
          </Button>
          <Button
            onClick={() => handleReview(4)}
            variant="ghost"
            className="col-span-1"
          >
            Easy
          </Button>
          <Button
            onClick={() => handleReview(5)}
            variant="primary"
            className="col-span-1"
          >
            ✓
          </Button>
        </div>
      )}

      {!isFlipped && (
        <div className="text-center">
          <Button onClick={handleFlip} className="bg-orange-500 hover:bg-orange-600">
            Reveal Answer
          </Button>
        </div>
      )}

      {/* Hint */}
      {!isFlipped && currentCard.cue && (
        <Card className="p-4 bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800">
          <p className="text-sm text-amber-800 dark:text-amber-200">
            <span className="font-semibold">Hint:</span> {currentCard.cue}
          </p>
        </Card>
      )}
    </div>
  );
}

interface FlashcardViewProps {
  card: Flashcard;
  isFlipped: boolean;
  onFlip: () => void;
  onSwipeLeft: () => void;
  onSwipeRight: () => void;
}

function FlashcardView({ card, isFlipped, onFlip, onSwipeLeft, onSwipeRight }: FlashcardViewProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [dragStart, setDragStart] = useState<{ x: number; y: number } | null>(null);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);

  const handleMouseDown = (e: React.MouseEvent) => {
    setDragStart({ x: e.clientX, y: e.clientY });
    setIsDragging(true);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!dragStart || !isDragging) return;

    const offsetX = e.clientX - dragStart.x;
    const offsetY = e.clientY - dragStart.y;
    setDragOffset({ x: offsetX, y: offsetY });
  };

  const handleMouseUp = () => {
    if (!isDragging) return;

    const threshold = 100;
    if (Math.abs(dragOffset.x) > threshold) {
      if (dragOffset.x > 0) {
        onSwipeRight();
      } else {
        onSwipeLeft();
      }
    }

    setDragStart(null);
    setDragOffset({ x: 0, y: 0 });
    setIsDragging(false);
  };

  const rotation = dragOffset.x * 0.1;
  const opacity = 1 - Math.abs(dragOffset.x) / 300;

  return (
    <div
      ref={cardRef}
      className="relative perspective-1000"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      style={{
        transform: `translateX(${dragOffset.x}px) translateY(${dragOffset.y}px) rotate(${rotation}deg)`,
        opacity,
        transition: isDragging ? 'none' : 'transform 0.3s ease, opacity 0.3s ease',
        cursor: isDragging ? 'grabbing' : 'grab',
      }}
    >
      <div
        className={`relative w-full h-96 transition-transform duration-500 transform-style-3d ${
          isFlipped ? 'rotate-y-180' : ''
        }`}
        onClick={!isDragging ? onFlip : undefined}
      >
        {/* Front */}
        <Card
          className={`absolute inset-0 backface-hidden flex items-center justify-center p-8 bg-gradient-to-br from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20 border-2 border-orange-200 dark:border-orange-800 ${
            isDragging ? 'cursor-grabbing' : 'cursor-pointer'
          }`}
        >
          <div className="text-center space-y-4">
            <div className="text-4xl">❓</div>
            <p className="text-xl font-medium text-gray-900 dark:text-white">{card.front}</p>
          </div>
        </Card>

        {/* Back */}
        <Card
          className={`absolute inset-0 backface-hidden rotate-y-180 flex items-center justify-center p-8 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-2 border-green-200 dark:border-green-800 ${
            isDragging ? 'cursor-grabbing' : 'cursor-pointer'
          }`}
        >
          <div className="text-center space-y-4">
            <div className="text-4xl">✓</div>
            <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
              {card.back}
            </p>
          </div>
        </Card>
      </div>

      {/* Swipe Indicators */}
      {isDragging && (
        <>
          {dragOffset.x > 50 && (
            <div className="absolute top-4 right-4 text-6xl animate-bounce">✓</div>
          )}
          {dragOffset.x < -50 && (
            <div className="absolute top-4 left-4 text-6xl animate-bounce">✗</div>
          )}
        </>
      )}
    </div>
  );
}

// Made with Bob
