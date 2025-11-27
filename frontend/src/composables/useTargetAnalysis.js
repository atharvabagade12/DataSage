
import { ref, computed } from 'vue';

export function useTargetAnalysis() {
  
  // ============================================================================
  // HELPER FUNCTIONS - Advanced Analysis
  // ============================================================================
  
  /**
   * Calculate Shannon Entropy - measures information content
   * Higher entropy = more information/variability (good for target)
   * Lower entropy = less information (poor for target)
   */
  const calculateEntropy = (values) => {
    if (!values || values.length === 0) return 0;
    
    const counts = {};
    values.forEach(val => {
      counts[val] = (counts[val] || 0) + 1;
    });
    
    const total = values.length;
    let entropy = 0;
    
    Object.values(counts).forEach(count => {
      const probability = count / total;
      if (probability > 0) {
        entropy -= probability * Math.log2(probability);
      }
    });
    
    return entropy;
  };

  /**
   * Calculate Gini Impurity - measures class imbalance
   * 0 = perfect balance, 1 = severe imbalance
   * Better than simple max ratio for multi-class problems
   */
  const calculateGiniImpurity = (distribution) => {
    if (!distribution || Object.keys(distribution).length === 0) return 1;
    
    let gini = 1;
    Object.values(distribution).forEach(ratio => {
      gini -= ratio * ratio;
    });
    
    return gini;
  };

  /**
   * Detect if column is a datetime/temporal column
   * These should NOT be recommended as targets
   */
  const isDateTimeColumn = (columnName, sampleValues) => {
    // Check column name for temporal keywords
    const temporalKeywords = [
      'date', 'time', 'datetime', 'timestamp', 'created', 'updated',
      'modified', 'year', 'month', 'day', 'hour', 'minute', 'second',
      'at', 'on', 'when', 'period', 'duration', 'start', 'end'
    ];
    
    const hasTemporalName = temporalKeywords.some(keyword => 
      columnName.toLowerCase().includes(keyword)
    );
    
    if (hasTemporalName) return true;
    
    // Check sample values for date patterns
    if (!sampleValues || sampleValues.length === 0) return false;
    
    const datePatterns = [
      /^\d{4}-\d{2}-\d{2}/, // ISO date: 2024-01-15
      /^\d{2}\/\d{2}\/\d{4}/, // US date: 01/15/2024
      /^\d{2}-\d{2}-\d{4}/, // EU date: 15-01-2024
      /^\d{4}\/\d{2}\/\d{2}/, // Alt ISO: 2024/01/15
      /T\d{2}:\d{2}:\d{2}/, // Time component: T14:30:00
    ];
    
    const dateMatches = sampleValues.filter(val => 
      datePatterns.some(pattern => pattern.test(String(val)))
    ).length;
    
    // If >50% of samples match date patterns, it's a datetime column
    return dateMatches / sampleValues.length > 0.5;
  };

  /**
   * Detect if column contains free text (descriptions, comments)
   * These are poor targets for ML
   */
  const isTextColumn = (sampleValues) => {
    if (!sampleValues || sampleValues.length === 0) return false;
    
    const textValues = sampleValues.filter(val => typeof val === 'string');
    if (textValues.length === 0) return false;
    
    // Calculate average text length
    const avgLength = textValues.reduce((sum, val) => sum + val.length, 0) / textValues.length;
    
    // Check for variance in length (free text has high variance)
    const lengths = textValues.map(val => val.length);
    const meanLength = avgLength;
    const variance = lengths.reduce((sum, len) => sum + Math.pow(len - meanLength, 2), 0) / lengths.length;
    const stdDev = Math.sqrt(variance);
    
    // Free text indicators:
    // 1. Average length > 50 characters
    // 2. High variance in length (stdDev > 20)
    // 3. Contains spaces (sentences/paragraphs)
    const hasSpaces = textValues.some(val => val.includes(' '));
    
    return avgLength > 50 || (stdDev > 20 && hasSpaces);
  };

  /**
   * Calculate cardinality score based on unique values ratio
   * Helps distinguish between good categorical targets and IDs/text
   */
  const calculateCardinalityScore = (uniqueValues, totalRows) => {
    const ratio = uniqueValues / totalRows;
    
    // Perfect binary (2 unique values)
    if (uniqueValues === 2) return 100;
    
    // Good multi-class (3-20 unique values)
    if (uniqueValues >= 3 && uniqueValues <= 20) return 85;
    
    // Moderate multi-class (21-50 unique values)
    if (uniqueValues >= 21 && uniqueValues <= 50) return 70;
    
    // High cardinality but reasonable (51-100 unique, <30% ratio)
    if (uniqueValues <= 100 && ratio < 0.3) return 50;
    
    // Very high cardinality (likely ID or free text)
    if (ratio > 0.5) return 10;
    
    // Default for edge cases
    return 40;
  };

  /**
   * Detect aggregated/derived features
   * These are usually not good targets
   */
  const isAggregatedFeature = (columnName) => {
    const aggregationPatterns = [
      '_mean', '_avg', '_average', '_sum', '_total', '_count', '_cnt',
      '_std', '_stddev', '_var', '_variance', '_min', '_max',
      '_median', '_mode', '_q1', '_q3', '_iqr', '_range',
      '_encoded', '_transformed', '_scaled', '_normalized',
      'avg_', 'sum_', 'count_', 'total_', 'mean_', 'std_',
      'min_', 'max_', 'median_'
    ];
    
    return aggregationPatterns.some(pattern => 
      columnName.toLowerCase().includes(pattern)
    );
  };

  /**
   * Detect outliers using IQR method
   */
  const detectOutliers = (numbers) => {
    if (numbers.length < 4) return [];
    const sorted = [...numbers].sort((a, b) => a - b);
    const q1 = sorted[Math.floor(sorted.length * 0.25)];
    const q3 = sorted[Math.floor(sorted.length * 0.75)];
    const iqr = q3 - q1;
    if (iqr === 0) return [];
    const lowerBound = q1 - 1.5 * iqr;
    const upperBound = q3 + 1.5 * iqr;
    return numbers.filter((n) => n < lowerBound || n > upperBound);
  };

  /**
   * Enhanced ID column detection
   */
  const isIDColumn = (analysis) => {
    const namePattern = /^(id|ID|.*_id|.*_ID|key|.*_key|uuid|guid|.*_uuid|.*_guid|index|idx)$/i;
    const uniqueRatio = analysis.uniqueValues / analysis.totalRows;
    
    // Check for UUID/GUID pattern in sample values
    const hasUUIDPattern = analysis.sampleValues?.some(val => 
      /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(String(val))
    );
    
    // Check for sequential numeric IDs
    const isSequential = analysis.type === 'number' && uniqueRatio > 0.95;
    
    // Check for high cardinality (>95% unique)
    const isHighCardinality = uniqueRatio > 0.95;
    
    return namePattern.test(analysis.name) || hasUUIDPattern || isSequential || isHighCardinality;
  };

  // ============================================================================
  // MAIN SCORING FUNCTION - Weighted Multi-Factor Analysis
  // ============================================================================
  
  const calculateTargetSuitability = (analysis) => {
    // Weighted scoring system
    const weights = {
      critical: 0.40,   // Must-have criteria (zero variance, IDs, encoding)
      important: 0.30,  // Strong indicators (balance, missing data, cardinality)
      helpful: 0.20,    // Good signals (name patterns, type suitability)
      bonus: 0.10       // Nice extras (distribution, entropy)
    };
    
    let criticalScore = 100;
    let importantScore = 100;
    let helpfulScore = 100;
    let bonusScore = 100;

    // ============================================================================
    // CRITICAL FACTORS (40% weight) - Deal breakers
    // ============================================================================
    
    // ❌ CRITICAL: Zero variance (constant column)
    if (analysis.uniqueValues === 1) {
      return 0; // Completely useless as target
    }

    // ❌ CRITICAL: Encoded columns should NOT be targets
    if (analysis.isEncoded) {
      if (analysis.encoding === "onehot") {
        criticalScore -= 90; // Massive penalty
      } else if (analysis.encoding === "label") {
        criticalScore -= 70;
      } else if (analysis.encoding === "binary") {
        criticalScore -= 65;
      } else if (analysis.encoding === "ordinal") {
        criticalScore -= 30; // Ordinal can sometimes be okay
      } else {
        criticalScore -= 60;
      }
    }

    // ❌ CRITICAL: ID columns (never good targets)
    if (isIDColumn(analysis)) {
      criticalScore -= 85;
    }

    // ❌ CRITICAL: DateTime columns
    if (analysis.isDateTime) {
      criticalScore -= 90;
    }

    // ❌ CRITICAL: Free text columns
    if (analysis.isTextColumn) {
      criticalScore -= 80;
    }

    // ❌ CRITICAL: Aggregated features
    if (isAggregatedFeature(analysis.name)) {
      criticalScore -= 70;
    }

    // ============================================================================
    // IMPORTANT FACTORS (30% weight) - Strong indicators
    // ============================================================================

    // ❌ IMPORTANT: High missing data
    if (analysis.missingPercent > 10) {
      const penalty = Math.min(analysis.missingPercent * 2, 80);
      importantScore -= penalty;
    }

    // ❌ IMPORTANT: Class imbalance (using Gini coefficient)
    if (analysis.giniImpurity !== undefined) {
      // Gini close to 0 = severe imbalance
      // Gini close to max = good balance
      const maxGini = 1 - (1 / Object.keys(analysis.classDistribution || {}).length);
      const balanceScore = (analysis.giniImpurity / maxGini) * 100;
      
      if (balanceScore < 30) {
        importantScore -= 60; // Severe imbalance
      } else if (balanceScore < 50) {
        importantScore -= 35; // Moderate imbalance
      } else if (balanceScore > 80) {
        importantScore += 20; // Excellent balance
      }
    }

    //  IMPORTANT: Cardinality score
    if (analysis.cardinalityScore !== undefined) {
      // Scale cardinality score to -50 to +50 range
      const cardinalityBonus = (analysis.cardinalityScore - 50);
      importantScore += cardinalityBonus;
    }

    // ============================================================================
    // HELPFUL FACTORS (20% weight) - Good signals
    // ============================================================================

    // HELPFUL: Type suitability
    if (!analysis.isEncoded) {
      if (analysis.originalType === "numerical" || analysis.type === "number") {
        helpfulScore += 40; // Great for regression
      }
      if (analysis.originalType === "categorical" || analysis.type === "string") {
        helpfulScore += 35; // Great for classification
      }
    }

    //  HELPFUL: Target-like names
    const targetKeywords = [
      "target", "label", "class", "outcome", "result", "success", "fail",
      "status", "category", "type", "grade", "score", "rating", "price",
      "amount", "value", "predict", "forecast", "response", "dependent",
      "output", "y", "salary", "income", "cost", "revenue", "profit"
    ];

    if (targetKeywords.some((keyword) => analysis.name.toLowerCase().includes(keyword))) {
      helpfulScore += 60;
    }

    //  HELPFUL: Business/Domain terms
    const businessKeywords = [
      "churn", "fraud", "default", "approved", "rejected", "conversion",
      "retention", "satisfaction", "quality", "performance", "efficiency",
      "risk", "demand", "sales", "growth", "attrition"
    ];

    if (businessKeywords.some((keyword) => analysis.name.toLowerCase().includes(keyword))) {
      helpfulScore += 45;
    }

    // ❌ HELPFUL: Underscore penalty (likely engineered features)
    if (analysis.name.includes("_") && !analysis.isEncoded) {
      helpfulScore -= 50;
    }

    // ============================================================================
    // BONUS FACTORS (10% weight) - Nice extras
    // ============================================================================

    //  BONUS: High entropy (good information content)
    if (analysis.entropy !== undefined) {
      // Normalize entropy to 0-100 scale (max entropy for binary is 1, for n-class is log2(n))
      const maxEntropy = Math.log2(Math.max(analysis.uniqueValues, 2));
      const entropyScore = (analysis.entropy / maxEntropy) * 100;
      
      if (entropyScore > 80) {
        bonusScore += 40; // Excellent variability
      } else if (entropyScore > 60) {
        bonusScore += 20; // Good variability
      } else if (entropyScore < 20) {
        bonusScore -= 30; // Poor variability
      }
    }

    //  BONUS: Good statistical distribution (for numeric)
    if (analysis.type === "number" && analysis.statistics && !analysis.isEncoded) {
      const { mean, median, std } = analysis.statistics;

      // Well-distributed data (mean ≈ median)
      if (std > 0 && Math.abs(mean - median) < std * 0.5) {
        bonusScore += 25;
      }

      // Reasonable variance (not constant)
      if (std / Math.abs(mean) > 0.1) {
        bonusScore += 15;
      }

      // ❌ PENALTY: Extreme skewness
      const skewness = Math.abs(mean - median) / (std || 1);
      if (skewness > 2) {
        bonusScore -= 40; // Highly skewed
      }
    }

    // ============================================================================
    // FINAL WEIGHTED SCORE CALCULATION
    // ============================================================================
    
    const finalScore = 
      (criticalScore * weights.critical) +
      (importantScore * weights.important) +
      (helpfulScore * weights.helpful) +
      (bonusScore * weights.bonus);

    return Math.max(0, Math.min(100, Math.round(finalScore)));
  };

  // ============================================================================
  // MAIN PROCESSING FUNCTION
  // ============================================================================
  
  const processColumns = (dataset, columns) => {
    if (!dataset || dataset.length === 0 || !columns || columns.length === 0) {
      return [];
    }

    const processed = columns.map((column) => {
      const columnName = column.name;
      const rawData = dataset.map((row) => row[columnName]);
      const cleanData = rawData.filter(
        (val) => val !== null && val !== undefined && val !== "" && val !== "null"
      );

      const missingCount = dataset.length - cleanData.length;
      const missingPercent = (missingCount / dataset.length) * 100;
      const uniqueValues = new Set(cleanData).size;

      let currentType = column.type || "categorical";
      let originalType = column.originalType || column.type || "categorical";

      const isEncodedColumn = Boolean(
        column.isEncoded ||
          column.encoding ||
          (columnName.includes("_") &&
            uniqueValues <= 2 &&
            cleanData.every((val) => [0, 1, "0", "1"].includes(val)))
      );

      let analysis = {
        name: columnName,
        originalType: originalType,
        type: currentType,
        missingPercent,
        missingValues: missingCount,
        totalRows: dataset.length,
        uniqueValues,
        sampleValues: cleanData.slice(0, 10),
        outliers: 0,
        statistics: null,
        encoding: column.encoding || "none",
        isEncoded: isEncodedColumn,
        hasEncoding: isEncodedColumn,
        classDistribution: null,
        
        // New advanced metrics
        entropy: 0,
        giniImpurity: undefined,
        cardinalityScore: 0,
        isDateTime: false,
        isTextColumn: false,
      };

      // Detect datetime columns
      analysis.isDateTime = isDateTimeColumn(columnName, cleanData);

      // Detect text columns
      analysis.isTextColumn = isTextColumn(cleanData);

      // Calculate entropy
      analysis.entropy = calculateEntropy(cleanData);

      // Calculate cardinality score
      analysis.cardinalityScore = calculateCardinalityScore(uniqueValues, dataset.length);

      // Process numeric columns
      if (currentType === "numerical" || currentType === "number") {
        const numbers = cleanData
          .map((val) => parseFloat(String(val).replace(/,/g, "")))
          .filter((n) => !isNaN(n) && isFinite(n));

        if (numbers.length > 0) {
          const mean = numbers.reduce((sum, n) => sum + n, 0) / numbers.length;
          const sorted = [...numbers].sort((a, b) => a - b);
          const median =
            numbers.length % 2 === 0
              ? (sorted[numbers.length / 2 - 1] + sorted[numbers.length / 2]) / 2
              : sorted[Math.floor(numbers.length / 2)];
          const std = Math.sqrt(
            numbers.reduce((sum, n) => sum + Math.pow(n - mean, 2), 0) /
              numbers.length
          );

          analysis.statistics = {
            min: Math.min(...numbers),
            max: Math.max(...numbers),
            mean,
            median,
            std,
          };
          analysis.outliers = detectOutliers(numbers).length;
        }
      }

      // Calculate class distribution and Gini for categorical columns
      if (currentType === "string" || currentType === "categorical") {
        const classCounts = {};
        cleanData.forEach(val => {
          classCounts[val] = (classCounts[val] || 0) + 1;
        });
        
        // Convert to ratios
        analysis.classDistribution = {};
        Object.keys(classCounts).forEach(key => {
          analysis.classDistribution[key] = classCounts[key] / cleanData.length;
        });
        
        // Calculate Gini impurity
        analysis.giniImpurity = calculateGiniImpurity(analysis.classDistribution);
      }

      // Calculate final suitability score
      analysis.suitabilityScore = calculateTargetSuitability(analysis);
      
      // Mark as recommended if score >= 70 and not encoded
      analysis.recommended = analysis.suitabilityScore >= 70 && !analysis.isEncoded;

      return analysis;
    });

    // Sort by suitability score (recommended first, then by score)
    return processed.sort((a, b) => {
      if (a.recommended !== b.recommended) {
        return b.recommended - a.recommended;
      }
      return b.suitabilityScore - a.suitabilityScore;
    });
  };

  return {
    processColumns,
    calculateTargetSuitability,
    detectOutliers,
    isIDColumn,
    calculateEntropy,
    calculateGiniImpurity,
    isDateTimeColumn,
    isTextColumn,
    calculateCardinalityScore,
    isAggregatedFeature
  };
}
