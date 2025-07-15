'use client';

import { useState } from 'react';
import { Search, Loader2, BookOpen } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';

interface Paper {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  published_date: string;
  journal: string;
  url: string;
}

export default function Home() {
  const { toast } = useToast();
  const [searchQuery, setSearchQuery] = useState('');
  const [papers, setPapers] = useState<Paper[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      toast({
        description: '검색어를 입력해주세요.',
        variant: 'destructive',
      });
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/papers/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchQuery }),
      });

      if (!response.ok) {
        throw new Error('검색 중 오류가 발생했습니다.');
      }

      const data = await response.json();
      setPapers(data.papers || []);
      
      if (data.papers?.length === 0) {
        toast({
          description: '검색 결과가 없습니다.',
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.');
      toast({
        description: '검색 중 오류가 발생했습니다.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Paper Glimpse
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              연구 분야를 검색하여 최신 논문을 찾아보세요
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 max-w-2xl mx-auto">
              <Input
                placeholder="연구 분야를 입력하세요 (예: machine learning, computer vision)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                className="flex-1 h-12 text-lg"
                disabled={isLoading}
              />
              <Button
                onClick={handleSearch}
                disabled={isLoading}
                className="h-12 px-8"
                size="lg"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                ) : (
                  <Search className="w-5 h-5 mr-2" />
                )}
                검색
              </Button>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {papers.length > 0 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold text-gray-900">
                검색 결과 ({papers.length}개)
              </h2>
              
              <div className="grid gap-6">
                {papers.map((paper) => (
                  <Card key={paper.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <CardTitle className="text-xl leading-tight pr-4">
                          <a
                            href={paper.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 hover:underline"
                          >
                            {paper.title}
                          </a>
                        </CardTitle>
                        <BookOpen className="w-5 h-5 text-gray-400 flex-shrink-0 mt-1" />
                      </div>
                      
                      <div className="flex flex-wrap items-center gap-2 text-sm text-gray-600">
                        <span>{paper.authors.join(', ')}</span>
                        <span>•</span>
                        <Badge variant="secondary">{paper.journal}</Badge>
                        <span>•</span>
                        <span>{new Date(paper.published_date).toLocaleDateString('ko-KR')}</span>
                      </div>
                    </CardHeader>
                    
                    <CardContent>
                      <p className="text-gray-700 leading-relaxed">
                        {paper.abstract.length > 300
                          ? `${paper.abstract.substring(0, 300)}...`
                          : paper.abstract}
                      </p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {!isLoading && papers.length === 0 && !error && (
            <div className="text-center py-12">
              <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-lg text-gray-500">
                검색어를 입력하여 논문을 찾아보세요
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
