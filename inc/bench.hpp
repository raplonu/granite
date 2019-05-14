#ifndef GRANITE_BENCH_HPP
#define GRANITE_BENCH_HPP
#pragma once

namespace granite {
    namespace bench {

        // TODO : Add donotoptimise
        // TODO : Add fast loop
        
        template<typename F>
        struct repeater_t
        {
            F f;
            int n;

            template<typename FP>
            repeater_t(FP&& fp, int n) : f(std::forward<FP>(fp)), n(n) {}

            template<typename... Args>
            void operator()(Args&&... args) {
                for(int i{}; i < n; ++i)
                    f(args);
            }

            template<typename... Args>
            void operator()(Args&&... args) const {
                for(int i{}; i < n; ++i)
                    f(args);
            }
        };

        template<typename F>
        repeater_t<F> repeater(F&& f, int n) {
            return repeater_t<F>(std::forward<F>(f), n);
        }


        template<typename Generator, typename Consumer>
        struct toto_guard {
            toto_guard(Generator g, Consumer c) : g(g), c(c), start(g()) {}

            ~toto_guard() {
                auto stop = g();

                c(start, stop);
            } 
        };

        

        

    }
}

#endif //GRANITE_BENCH_HPP