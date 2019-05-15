#ifndef GRANITE_BENCH_HPP
#define GRANITE_BENCH_HPP
#pragma once

namespace granite {
    namespace bench {

        // TODO : Add donotoptimise
        // TODO : Add fast loop
        struct counter_predicate {
            int count;

            constexpr bool operator()() noexcept {
                return count--;
            }
        };

        template<typename F, typename P>
        struct multi_function_call_t {
            F f;
            P p;

            void operator()() {
                while(p())
                    f();
            }
        };

        template<typename F, typename P>
        constexpr auto multi_function_call(F && f, P && p) -> multi_function_call_t<F, P> {
            return { std::forward<F>(f), std::forward<P>(p) };
        }

        template<typename F>
        constexpr auto repeat_function_call(F && f, int n)
            -> multi_function_call_t<F, counter_predicate>
        {
            return { std::forward<F>(f), { n } };
        }



        template<typename G, typename It>
        struct bench_guard_t {
            G g;
            It it;
            const auto start = g();

            ~bench_guard_t() {
                const auto stop = g();

                *it = stop - start;
            } 
        };


        template<typename >
        struct BenchIt {


            auto operator()(auto input) {
                auto bg = bench_guard(g, out_it);
                f();

            }
        };
        

        

    }
}

#endif //GRANITE_BENCH_HPP