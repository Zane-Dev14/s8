"use client";

import { useEffect, useState } from "react";
import { ArrowLeft, BookOpen, CheckCircle2, Circle, Loader2, Trophy, Clock, Target, Zap, Sparkles, Brain, Award } from "lucide-react";
import { Card, CardText, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface Concept {
  id: string;
  name: string;
  plain_name: string;
  explanation?: string;
  difficulty: string;
  mastered?: boolean;
  module?: string;
  metadata?: {
    exam_importance?: number;
    pyq_frequency?: string;
    marks_pattern?: string;
    time_to_learn?: string;
  };
}

interface ConceptListProps {
  subjectId: string;
  subjectName: string;
  onSelectConcept: (conceptId: string, conceptName: string) => void;
  onBack: () => void;
}

export function ConceptList({ subjectId, subjectName, onSelectConcept, onBack }: ConceptListProps) {
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedModule, setSelectedModule] = useState<string | null>(null);
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/subjects/${subjectId}/concepts`)
      .then((res) => res.json())
      .then((data) => {
        const parsedConcepts = (data || []).map((concept: any) => ({
          ...concept,
          metadata: typeof concept.metadata_json === 'string' 
            ? JSON.parse(concept.metadata_json || '{}')
            : concept.metadata_json || {}
        }));
        setConcepts(parsedConcepts);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to load concepts");
        setLoading(false);
      });
  }, [subjectId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-center">
          <div className="relative">
            <Loader2 className="w-16 h-16 animate-spin text-purple-400 mx-auto mb-4" />
            <Sparkles className="w-8 h-8 text-yellow-400 absolute top-0 right-0 animate-pulse" />
          </div>
          <p className="text-xl text-purple-200 font-medium animate-pulse">Loading concepts...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <Card className="p-8 max-w-md bg-slate-800/50 backdrop-blur-xl border-red-500/50">
          <CardTitle className="text-red-400 mb-4">Error</CardTitle>
          <CardText className="text-slate-300">{error}</CardText>
          <Button onClick={onBack} className="mt-4 bg-purple-600 hover:bg-purple-700">Go Back</Button>
        </Card>
      </div>
    );
  }

  const moduleGroups = concepts.reduce((acc, concept) => {
    const module = concept.module || "Other";
    if (!acc[module]) acc[module] = [];
    acc[module].push(concept);
    return acc;
  }, {} as Record<string, Concept[]>);

  const modules = Object.keys(moduleGroups).sort();
  const displayModules = selectedModule ? [selectedModule] : modules;

  const difficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case "beginner":
        return "bg-emerald-500/20 text-emerald-300 border-emerald-500/50";
      case "intermediate":
        return "bg-amber-500/20 text-amber-300 border-amber-500/50";
      case "advanced":
        return "bg-rose-500/20 text-rose-300 border-rose-500/50";
      default:
        return "bg-slate-500/20 text-slate-300 border-slate-500/50";
    }
  };

  const importanceStars = (importance: number = 3) => {
    return "⭐".repeat(Math.min(importance, 5));
  };

  const totalConcepts = concepts.length;
  const masteredCount = concepts.filter(c => c.mastered).length;
  const progressPercent = totalConcepts > 0 ? Math.round((masteredCount / totalConcepts) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-pink-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <div className="mb-8 animate-fade-in">
          <Button
            variant="ghost"
            onClick={onBack}
            className="mb-4 text-purple-300 hover:text-purple-100 hover:bg-purple-800/30 transition-all duration-300"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Subjects
          </Button>
          
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-purple-500/20 hover:border-purple-500/40 transition-all duration-500">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-3">
                  <Brain className="w-10 h-10 text-purple-400 animate-pulse" />
                  <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
                    {subjectName}
                  </h1>
                </div>
                <p className="text-lg text-slate-300 mb-6">
                  Master concepts module by module with exam-focused learning 🚀
                </p>
                
                {/* Stats */}
                <div className="flex flex-wrap gap-4">
                  <div className="flex items-center gap-3 bg-purple-500/20 px-5 py-3 rounded-xl border border-purple-500/30 hover:scale-105 transition-transform duration-300">
                    <BookOpen className="w-6 h-6 text-purple-300" />
                    <div>
                      <div className="text-2xl font-bold text-purple-200">{totalConcepts}</div>
                      <div className="text-xs text-purple-400">Concepts</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 bg-emerald-500/20 px-5 py-3 rounded-xl border border-emerald-500/30 hover:scale-105 transition-transform duration-300">
                    <Trophy className="w-6 h-6 text-emerald-300" />
                    <div>
                      <div className="text-2xl font-bold text-emerald-200">{masteredCount}</div>
                      <div className="text-xs text-emerald-400">Mastered</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 bg-blue-500/20 px-5 py-3 rounded-xl border border-blue-500/30 hover:scale-105 transition-transform duration-300">
                    <Target className="w-6 h-6 text-blue-300" />
                    <div>
                      <div className="text-2xl font-bold text-blue-200">{progressPercent}%</div>
                      <div className="text-xs text-blue-400">Complete</div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Progress Circle */}
              <div className="relative w-32 h-32">
                <svg className="transform -rotate-90 w-32 h-32">
                  <circle
                    cx="64"
                    cy="64"
                    r="56"
                    stroke="currentColor"
                    strokeWidth="8"
                    fill="transparent"
                    className="text-slate-700"
                  />
                  <circle
                    cx="64"
                    cy="64"
                    r="56"
                    stroke="currentColor"
                    strokeWidth="8"
                    fill="transparent"
                    strokeDasharray={`${2 * Math.PI * 56}`}
                    strokeDashoffset={`${2 * Math.PI * 56 * (1 - progressPercent / 100)}`}
                    className="text-purple-400 transition-all duration-1000 ease-out"
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-200">{progressPercent}%</div>
                    <Award className="w-6 h-6 text-yellow-400 mx-auto mt-1" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Module Filter */}
        {modules.length > 1 && (
          <div className="mb-6 flex flex-wrap gap-3 animate-slide-up">
            <Button
              variant={selectedModule === null ? "primary" : "ghost"}
              onClick={() => setSelectedModule(null)}
              className={`${
                selectedModule === null 
                  ? "bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/50" 
                  : "bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 border border-slate-700"
              } transition-all duration-300 hover:scale-105`}
            >
              All Modules
            </Button>
            {modules.map((module) => (
              <Button
                key={module}
                variant={selectedModule === module ? "primary" : "ghost"}
                onClick={() => setSelectedModule(module)}
                className={`${
                  selectedModule === module 
                    ? "bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/50" 
                    : "bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 border border-slate-700"
                } transition-all duration-300 hover:scale-105`}
              >
                {module} ({moduleGroups[module].length})
              </Button>
            ))}
          </div>
        )}

        {/* Concepts by Module */}
        {displayModules.map((module, moduleIndex) => (
          <div key={module} className="mb-8 animate-slide-up" style={{ animationDelay: `${moduleIndex * 100}ms` }}>
            <div className="flex items-center gap-3 mb-4">
              <div className="h-1 w-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"></div>
              <h2 className="text-3xl font-bold text-slate-100">{module}</h2>
              <Badge tone="neutral" className="ml-2 bg-purple-500/20 text-purple-300 border border-purple-500/30">
                {moduleGroups[module].length} concepts
              </Badge>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {moduleGroups[module].map((concept, index) => (
                <Card
                  key={concept.id}
                  className={`group bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:border-purple-500/50 transition-all duration-500 overflow-hidden animate-fade-in ${
                    hoveredCard === concept.id ? 'scale-105 shadow-2xl shadow-purple-500/30' : 'hover:scale-102'
                  }`}
                  style={{ animationDelay: `${index * 50}ms` }}
                  onMouseEnter={() => setHoveredCard(concept.id)}
                  onMouseLeave={() => setHoveredCard(null)}
                >
                  <div className="p-6 relative">
                    {/* Glow effect on hover */}
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-500/0 via-purple-500/5 to-pink-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                    
                    {/* Header */}
                    <div className="flex items-start justify-between mb-3 relative z-10">
                      <div className="flex items-start gap-3 flex-1">
                        {concept.mastered ? (
                          <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0 mt-1 animate-pulse" />
                        ) : (
                          <Circle className="w-6 h-6 text-slate-600 flex-shrink-0 mt-1 group-hover:text-purple-400 transition-colors duration-300" />
                        )}
                        <div className="flex-1">
                          <CardTitle className="text-lg text-slate-100 group-hover:text-purple-300 transition-colors duration-300">
                            {concept.plain_name || concept.name}
                          </CardTitle>
                          {concept.explanation && (
                            <CardText className="text-sm text-slate-400 mt-2 line-clamp-2 group-hover:text-slate-300 transition-colors duration-300">
                              {concept.explanation}
                            </CardText>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Metadata Tags */}
                    <div className="flex flex-wrap gap-2 mt-4 relative z-10">
                      <Badge className={`${difficultyColor(concept.difficulty)} border transition-all duration-300 group-hover:scale-105`}>
                        {concept.difficulty}
                      </Badge>
                      
                      {concept.metadata?.exam_importance && (
                        <Badge tone="warning" className="bg-yellow-500/20 text-yellow-300 border border-yellow-500/30 transition-all duration-300 group-hover:scale-105">
                          {importanceStars(concept.metadata.exam_importance)}
                        </Badge>
                      )}
                      
                      {concept.metadata?.pyq_frequency && (
                        <Badge tone="neutral" className="bg-blue-500/20 text-blue-300 border border-blue-500/30 transition-all duration-300 group-hover:scale-105">
                          <Zap className="w-3 h-3 mr-1" />
                          PYQ: {concept.metadata.pyq_frequency}
                        </Badge>
                      )}
                      
                      {concept.metadata?.time_to_learn && (
                        <Badge tone="neutral" className="bg-purple-500/20 text-purple-300 border border-purple-500/30 transition-all duration-300 group-hover:scale-105">
                          <Clock className="w-3 h-3 mr-1" />
                          {concept.metadata.time_to_learn}
                        </Badge>
                      )}
                      
                      {concept.mastered && (
                        <Badge tone="success" className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 animate-pulse">
                          ✓ Mastered
                        </Badge>
                      )}
                    </div>

                    {/* Marks Pattern */}
                    {concept.metadata?.marks_pattern && (
                      <div className="mt-3 text-xs text-slate-500 bg-slate-900/50 px-3 py-2 rounded-lg border border-slate-700 relative z-10">
                        📝 {concept.metadata.marks_pattern}
                      </div>
                    )}

                    {/* Action Button */}
                    <Button
                      type="button"
                      className="w-full mt-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-500/30 transition-all duration-300 group-hover:shadow-purple-500/50 relative z-10"
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        console.log('Navigating to concept:', concept.id, concept.plain_name || concept.name);
                        onSelectConcept(concept.id, concept.plain_name || concept.name);
                      }}
                    >
                      <BookOpen className="w-4 h-4 mr-2" />
                      Start Learning
                      <Sparkles className="w-4 h-4 ml-2 animate-pulse" />
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        ))}

        {concepts.length === 0 && (
          <Card className="p-12 text-center bg-slate-800/50 backdrop-blur-xl border-slate-700 shadow-2xl animate-fade-in">
            <div className="text-6xl mb-4 animate-bounce">📚</div>
            <CardTitle className="mb-4 text-2xl text-slate-100">No Concepts Yet</CardTitle>
            <CardText className="text-lg text-slate-400">
              This subject doesn't have any concepts yet. Upload materials to get started!
            </CardText>
          </Card>
        )}
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fade-in {
          animation: fade-in 0.6s ease-out forwards;
        }

        .animate-slide-up {
          animation: slide-up 0.6s ease-out forwards;
        }

        .hover\:scale-102:hover {
          transform: scale(1.02);
        }
      `}</style>
    </div>
  );
}

// Made with Bob
