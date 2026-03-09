#!/usr/bin/env python3
"""
PDF字数统计工具
功能：计算PDF文件中的总字数
用法：python pdf_word_counter.py <pdf_file_path>
"""

import argparse
import pdfplumber
import PyPDF2
import re


def count_pdf_words_enhanced(pdf_path: str) -> tuple[int, int]:
    """
    使用pdfplumber计算PDF文件的总字数和字符数

    Args:
        pdf_path: PDF文件路径

    Returns:
        tuple: (总字数, 总字符数)
    """
    total_words = 0
    total_chars = 0

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text:  # 确保页面有文本内容
                    # 清理文本
                    clean_text = re.sub(r"\s+", " ", text).strip()

                    # 统计字符数（不包括空格）
                    chars = re.sub(r"\s", "", clean_text)
                    total_chars += len(chars)

                    # 统计字数（英文按单词，中文按字符）
                    # 英文单词
                    english_words = re.findall(r"\b[a-zA-Z]+\b", text)
                    # 中文词语（单个汉字也算作一个词）
                    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)

                    total_words += len(english_words) + len(chinese_chars)

    except FileNotFoundError:
        print(f"错误：找不到文件 {pdf_path}")
        return 0, 0
    except Exception as e:
        print(f"读取PDF文件时出错：{str(e)}")
        return 0, 0

    return total_words, total_chars


def count_pdf_words_basic(pdf_path: str) -> tuple[int, int]:
    """
    使用PyPDF2计算PDF文件的总字数和字符数（基础版本）

    Args:
        pdf_path: PDF文件路径

    Returns:
        tuple: (总字数, 总字符数)
    """

    total_words = 0
    total_chars = 0

    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                # 提取纯文本内容，去除多余空白字符
                clean_text = re.sub(r"\s+", " ", text).strip()

                # 统计字符数（不包括空格）
                chars = re.sub(r"\s", "", clean_text)
                total_chars += len(chars)

                # 统计字数（英文按单词，中文按字符）
                # 英文单词
                english_words = re.findall(r"\b[a-zA-Z]+\b", text)
                # 中文词语（单个汉字也算作一个词）
                chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)

                total_words += len(english_words) + len(chinese_chars)

    except FileNotFoundError:
        print(f"错误：找不到文件 {pdf_path}")
        return 0, 0
    except Exception as e:
        print(f"读取PDF文件时出错：{str(e)}")
        return 0, 0

    return total_words, total_chars


def main():
    """主函数 - 解析命令行参数并执行字数统计"""
    parser = argparse.ArgumentParser(
        description="PDF字数统计工具 - 准确计算PDF文档中的字数和字符数",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用说明:
  python pdf_word_counter.py example.pdf              # 使用基础引擎
  python pdf_word_counter.py example.pdf --engine enhanced  # 使用增强引擎

统计规则说明:
  📝 字数统计: 英文按单词计算，中文按字符计算
  🔤 字符数统计: 不包括空格在内的所有字符 (字母、数字、标点符号、中文字符等)
  💡 字数 = 英文单词数 + 中文字符数
        """,
    )
    parser.add_argument("pdf_file", help="PDF文件路径")
    parser.add_argument(
        "--engine",
        choices=["basic", "enhanced"],
        default="basic",
        help="选择PDF解析引擎 (basic: PyPDF2, enhanced: pdfplumber)",
    )

    args = parser.parse_args()

    print(f"正在分析PDF文件: {args.pdf_file}")
    print(f"使用解析引擎: {args.engine}")
    print("-" * 50)

    if args.engine == "enhanced":
        word_count, char_count = count_pdf_words_enhanced(args.pdf_file)
    else:
        word_count, char_count = count_pdf_words_basic(args.pdf_file)

    if word_count > 0 or char_count > 0:
        print(f"✅ PDF文件 '{args.pdf_file}' 统计完成!")
        print(f"📊 字数统计: {word_count:,} 字")
        print(f"📊 字符数统计: {char_count:,} 字符 (不含空格)")
        print(f"ℹ️  字数统计规则: 英文按单词计算，中文按字符计算")
        print(f"ℹ️  字符数统计规则: 统计所有非空白字符 (字母、数字、标点、中文字符等)")
        print(f"ℹ️  计算公式: 字数 = 英文单词数 + 中文字符数")
    else:
        print("❌ 未能成功统计字数，请检查:")
        print("   • 文件是否存在")
        print("   • 文件是否为有效的PDF格式")
        print("   • 文件是否受密码保护")
        print("   • 是否已安装所需依赖库")


if __name__ == "__main__":
    main()
